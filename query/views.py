# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")


def location(request, loc_x, loc_y):
    floc_x = float(loc_x)
    floc_y = float(loc_y)

    class Result(DjangoJSONEncoder):
        x = 0.0
        y = 0.0

    res = Result()
    res.x = floc_x
    res.y = floc_y
    return JsonResponse({"x": res.x, "y": res.y})
