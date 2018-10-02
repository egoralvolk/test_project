from rest_framework import serializers
from service.models import SIZE_OF_PASSPORT_NUMBER, SIZE_OF_PASSPORT_SERIES, SIZE_OF_PART_NAME
from service.models import IdentificationAttempt, IdentifiablePerson
from service import checker


class IdentifiablePersonSerializer(serializers.Serializer):
    passport_series = serializers.CharField(max_length=SIZE_OF_PASSPORT_SERIES, allow_blank=True)
    passport_number = serializers.CharField(max_length=SIZE_OF_PASSPORT_NUMBER, allow_blank=True)
    first_name = serializers.CharField(max_length=SIZE_OF_PART_NAME, allow_blank=True)
    middle_name = serializers.CharField(max_length=SIZE_OF_PART_NAME, allow_blank=True)
    last_name = serializers.CharField(max_length=SIZE_OF_PART_NAME, allow_blank=True)
    birthday = serializers.DateField(format=None)

    def validate_passport_series(self, series):
        message, ok = checker.check_passport_series(series)
        if not ok:
            raise serializers.ValidationError(message)
        return series

    def validate_passport_number(self, number):
        message, ok = checker.check_passport_number(number)
        if not ok:
            raise serializers.ValidationError(message)
        return number

    def validate_first_name(self, first_name):
        message, ok = checker.check_part_of_name(first_name)
        if not ok:
            raise serializers.ValidationError(message)
        return first_name

    def validate_middle_name(self, middle_name):
        message, ok = checker.check_part_of_name(middle_name)
        if not ok:
            raise serializers.ValidationError(message)
        return middle_name

    def validate_last_name(self, last_name):
        message, ok = checker.check_part_of_name(last_name)
        if not ok:
            raise serializers.ValidationError(message)
        return last_name

    def validate_birthday(self, birthday):
        message, ok = checker.check_birthday(birthday)
        if not ok:
            raise serializers.ValidationError(message)
        return birthday

    def create(self, validated_data):
        person = IdentifiablePerson.objects.filter(**validated_data).count()
        if person != 0:
            return IdentifiablePerson.objects.get(**validated_data)
        return IdentifiablePerson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass