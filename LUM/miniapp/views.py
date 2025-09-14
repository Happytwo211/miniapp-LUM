from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView
from .models import *
import json


class TourList(ListView):
    model = Tour
    ordering = 'tour_name'
    template_name = 'tours_list.html'
    context_object_name = 'tours'
    paginate_by = 3


class TourDetail(DetailView):
    model = Tour
    template_name = 'tour_detail.html'
    context_object_name = 'tour'

class StoryList(ListView):
    model = Story
    ordering = 'created_at'
    context_object_name = 'stories'
    template_name = 'story.html'

class TourDropDownElementsListView(ListView):
    model = TourDropDownElements
    ordering = 'element_created_at'
    context_object_name = 'drop_down_el'
    template_name = 'tours_list.html'

class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'phone_number']
    template_name = 'profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_id = data.get("user_id")
        username = data.get("username")

        user, created = User.objects.get_or_create(username=username or f"user_{user_id}")
        profile = user.profile
        profile.first_name = data.get("first_name", "")
        profile.last_name = data.get("last_name", "")
        profile.avatar_url = data.get("avatar_url", "")
        profile.phone_number = data.get("phone_number", "")
        profile.save()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)