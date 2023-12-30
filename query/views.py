# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.generic import TemplateView
from . import logic

picture_name = b"picture.jpg"


# Create your views here.
def index(_):
    return HttpResponse(b"Hello, world!")


def location(_, loc_x, loc_y):
    floc_x = float(loc_x)
    floc_y = float(loc_y)
    bolded_map, description = logic.query(floc_x, floc_y)
    print(description)

    map_rgb = bolded_map.convert('RGB')
    map_rgb.save(picture_name, "JPEG")

    return JsonResponse({"description": description})


def pipe_map(_):
    map = open(picture_name, 'rb')
    response = FileResponse(map)
    return response


class HomePageView(TemplateView):
    template_name = "index.html"
