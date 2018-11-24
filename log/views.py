from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize, deserialize
from log.models import Day, CheckFromShop
import json
import datetime
import json


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
        str_date = data["date"]
        try:
            datetime.datetime.strptime(str_date, "%Y-%m-%d")
        except:
            return HttpResponse(json.dumps([]))
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''
            SELECT log_checkfromshop.id, total, log_shop."name", date
            FROM log_checkfromshop
            LEFT JOIN log_shop 
            ON log_shop.id = log_checkfromshop.shop_id
            WHERE date = %s''', [str_date])
        desc = cursor.description
        rows = [dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()]
        print(json.dumps(rows, default=str))

        return HttpResponse(json.dumps(rows, default=str))
    else:
        return HttpResponse("test")
