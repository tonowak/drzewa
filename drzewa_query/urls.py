from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="drzewa_main"),
    path("desc/<str:loc_x>/<str:loc_y>/", views.desc, name="drzewa_desc"),
    path("image/<str:loc_x>/<str:loc_y>/", views.image, name="drzewa_image"),
]
