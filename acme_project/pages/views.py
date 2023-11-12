from typing import Any
from django.views.generic import TemplateView

from birthday.models import Birthday


class HomePage(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['total_count'] = Birthday.objects.count()
        return context
