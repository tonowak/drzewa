# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from . import logic


# Create your views here.
def index(_):
    return HttpResponse(b"Hello, world!")


def location(_, loc_x, loc_y):
    save_loc = 'static/' + loc_x + ';' + loc_y + '.jpg'

    floc_x = float(loc_x)
    floc_y = float(loc_y)
    bolded_map, description = logic.query(floc_x, floc_y)
    rgb_map = bolded_map.convert('RGB')
    rgb_map.save(settings.BASE_DIR / save_loc, 'JPEG')

    return JsonResponse({
        "description": description,
        "image_src": '/' + save_loc})


class HomePageView(TemplateView):
    template_name = "index.html"
