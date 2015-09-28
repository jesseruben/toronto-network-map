from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.conf import settings


class IndexView(TemplateView):
    template_name = 'index.html'

    def render_to_response(self, context, **response_kwargs):
        context['DEBUG'] = settings.DEBUG
        response = super(IndexView, self).render_to_response(context, **response_kwargs)
        return response

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)
