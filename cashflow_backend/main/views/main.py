from django.http import JsonResponse

def main(request):
    return JsonResponse({"mssg":"hello"})