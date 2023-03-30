from django.http import JsonResponse


def custom_response(data=None, success=False, message=None):
    return JsonResponse(
        {
            'data': data,
            'success': success,
            'message': message,
        }
    )