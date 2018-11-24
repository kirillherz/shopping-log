from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize, deserialize
from log.models import Day, CheckFromShop
import json
import datetime



def show_checks(request):
    return render(request, 'show_checks.html')


def get_json(request):
    if request.is_ajax():
        data = serialize(
            'json', Day.objects.all(), fields=('date', 'total'))
        return HttpResponse(data)
    else:
        return HttpResponse("ERROR")


def get_checks(request):
    if request.is_ajax():
        data = json.loads(request.POST.get("json")) 
        try:
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d")
        except:
            return HttpResponse(json.dumps([]))
        return HttpResponse(CheckFromShop.json.all(date))
    else:
        return HttpResponse("test")
