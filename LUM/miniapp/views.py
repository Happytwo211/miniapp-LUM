from django.views.generic import DetailView, ListView
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


