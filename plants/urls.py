from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import PlantDetailView

app_name = 'plants'

urlpatterns = [
    # ex: /plants/
    path('', views.db_view, name='db_view'),
    path('tag/<slug:tag_slug>/', views.db_view, name='db_view_by_tag'),
    path('<slug:slug>/', PlantDetailView.as_view(), name='plant_detail'),
    path('get-main-image/<slug:slug>/', PlantDetailView.as_view(), {'action': 'get_main_image'}, name='get_main_image'),
    path('get-carousel-images/<slug:slug>/', PlantDetailView.as_view(), {'action': 'get_carousel_images'}, name='get_carousel_images'),
    path('<slug:slug>/comment/', login_required(views.plant_comment), name='plant_comment'),
    path('<slug:slug>/tag/', login_required(views.plant_tag), name='plant_tag'),
]
