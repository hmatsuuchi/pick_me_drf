from django.views.generic import TemplateView

# LOGIN
class MainSpaView(TemplateView):
    template_name = "main-spa/main-spa-view/index.html"