# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from . import logic
import io

def main(request):
    return render(request, 'drzewa/index.html')

def desc(_, loc_x, loc_y):
    floc_x = float(loc_x)
    floc_y = float(loc_y)
    # TODO: handle exceptions from `logic`
    description = logic.query_desc(floc_x, floc_y)
    return JsonResponse({
        "description": description,
    })

def image(_, loc_x, loc_y):
    floc_x = float(loc_x)
    floc_y = float(loc_y)
    # TODO: handle exceptions from `logic`
    bolded_map = logic.query_image(floc_x, floc_y)
    image = io.BytesIO()
    bolded_map.save(image, format='png')
    return HttpResponse(image.getvalue(), content_type="image/png")
