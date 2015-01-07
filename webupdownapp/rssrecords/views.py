from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Rssrecord

class RssRecordList(ListView):
    model = Rssrecord
    template_name = 'rssrecords/rssrecords_list.html'
    context_object_name = 'rssrecords'

    def get_queryset(self):
        account_list = Rssrecord.objects.filter(owner=self.request.user)
        return account_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RssRecordList, self).dispatch(*args, **kwargs)