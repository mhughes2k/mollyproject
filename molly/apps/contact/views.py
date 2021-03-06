import simplejson
import hashlib
import urllib2

from django.http import HttpResponse

from molly.utils.views import BaseView
from molly.utils.breadcrumbs import *
from molly.apps.contact.providers import TooManyResults

from .forms import GenericContactForm


class IndexView(BaseView):

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            'Contact search',
            lazy_reverse('index'),
        )

    def initial_context(self, request):
        return {
            'form': self.conf.provider.form(request.GET or None),
            'medium_choices': self.conf.provider.medium_choices,
        }

    def handle_GET(self, request, context):
        return self.render(request, context, 'contact/index')


class ResultListView(IndexView):

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            'Contact search',
            lazy_reverse('result_list'),
        )

    def handle_GET(self, request, context):
        provider = self.conf.provider

        form = provider.form(request.GET or None)
        medium = request.GET.get('medium')
        if not medium in [m[0] for m in provider.medium_choices]:
            medium = provider.medium_choices[0][0]

        if form.is_valid():

            query = provider.normalize_query(form.cleaned_data, medium)

            try:
                people = provider.perform_query(**query)
            except TooManyResults:
                return self.handle_error(request, context,
                                         "Your search returned too many results.")

            context.update({
                'results': people,
                'medium': medium,
            })

        context['form'] = form
        return self.render(request, context, 'contact/result_list')

    def handle_error(self, request, context, message):
        context.update({
            'message': message,
        })

        return self.render(request, context, 'contact/result_list')


class ResultDetailView(BaseView):

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            'Contact search',
            lazy_reverse('result_detail'),
        )

    def handle_GET(self, request, context, id):
        try:
            context['result'] = self.conf.provider.fetch_result(id)
        except BaseContactProvider.NoSuchResult:
            raise Http404

        return self.render(request, context, 'contact/result_detail')
