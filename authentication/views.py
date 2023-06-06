from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# LOGIN
class SessionLoginView(TemplateView):
    template_name = "authentication/session-login/index.html"

# LOGOUT
class SessionLogoutView(TemplateView):
    template_name = "authentication/session-logout/index.html"

# AUTHENTICATE
class SessionAuthenticateView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'login successful')
            login(request, user)
            return redirect('/authentication/session-login') # TEMPORARY REDIRECT
        else:
            messages.error(request, 'invalid username or password')

        return render(request, 'authentication/session-login/index.html') # TEMPORARY REDIRECT