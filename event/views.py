from django.views.generic import TemplateView

# LOGIN
class EventView(TemplateView):
    template_name = "event/event-view/index.html"
