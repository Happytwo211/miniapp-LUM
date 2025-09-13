from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView
from .models import *


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