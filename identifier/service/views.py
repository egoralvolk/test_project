import copy
import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view

from service.serializers import IdentifiablePersonSerializer
from service.models import IdentificationAttempt
from service.checker import check_person


@api_view(['POST'])
def persons(request):
    if request.method == 'POST':
        data = copy.deepcopy(request.data)
        if data['birthday'] == '':
            data['birthday'] = str(datetime.date(1, 1, 1))
        serializer = IdentifiablePersonSerializer(data=data)
        if serializer.is_valid():
            response = 'Идентификация прошла успешно'
            status = 200
            msg, ok = check_person(data)
            person = serializer.save()
            if not ok:
                response = 'Идентификация не пройдена:<br>' + msg
                status = 400
            IdentificationAttempt.objects.create(person=person, response=ok)
            return HttpResponse(response, status=status)
        else:
            response = 'Идентификация не пройдена:<br>'
            for value in serializer.errors.values():
                response += str(value[0]) + '<br>'

            return HttpResponse(response, status=400)


def index(request):
    return render(request, 'index.html')
