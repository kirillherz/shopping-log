from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from log.models import Day

# Create your views here.
def get_json(request):
    if request.is_ajax():
        data = serialize(
            'json', Day.objects.all(), fields=('date', 'total'))
        return HttpResponse(data)
    else:
        return HttpResponse("ERROR")
