from django.urls import path, include
from .views import *
urlpatterns = [
    path('tours_list/', TourList.as_view(), name='tour-list'),
    path('tour/<int:pk>', TourDetail.as_view(), name='tour-detail'),
    path('profile/<int:pk>', ProfileDetail.as_view(), name='profile'),
    path("api/update_profile/", update_profile, name="update_profile"),
    path("quiz/<int:pk>/", QuizDetail.as_view(), name="quiz_detail"),
    path("quiz/<int:pk>/submit/", QuizSubmit.as_view(), name="quiz_submit"),
    path("quiz/result/<int:pk>/", QuizResultDetail.as_view(), name="quiz_result"),

]

