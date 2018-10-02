function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function () {
    // var date = $('#birthday').datepicker({dateFormat: 'yy-mm-dd'}).val();
    $('#identificate-person').submit(function (e) {
        e.preventDefault();
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
        $.ajax({
            url: 'person',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'passport_series' : $('#passport_series').val(),
                'passport_number' : $('#passport_number').val(),
                'first_name' : $('#first_name').val(),
                'middle_name' : $('#middle_name').val(),
                'last_name' : $('#last_name').val(),
                'birthday' : $('#birthday').val(),
            }),
            dataType: 'json',
            cache: true,
            success: function (data) {
                $('#result-identification').html(data.response);
                console.log('success of identification');
                console.log(data);
            },
            error: function (error_data) {
                $('#result-identification').html(error_data.responseText);
                console.log(error_data.responseText);
                console.log(error_data);
            },
        });
    });
});
