from django.urls import path, include
from .views import *
urlpatterns = [
    path('tours_list/', TourList.as_view(), name='tour-list'),
    path('tour/<int:pk>', TourDetail.as_view(), name='tour-detail'),

]

