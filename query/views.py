# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import logic


# Create your views here.
def index(request):
    return HttpResponse(b"Hello, world!")


def location(request, loc_x, loc_y):
    floc_x = float(loc_x)
    floc_y = float(loc_y)
    bolded_map, description = logic.query(floc_x, floc_y)
    print(description)

    return JsonResponse({"description": description})
