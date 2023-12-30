from django.urls import path

from . import views

urlpatterns = [
    path("desc/<str:loc_x>/<str:loc_y>/", views.desc, name="desc"),
    path("image/<str:loc_x>/<str:loc_y>/", views.image, name="image"),
]
