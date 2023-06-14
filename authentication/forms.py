from django import forms

class SessionAuthenticationForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput())
    password = forms.CharField(label="password", widget=forms.PasswordInput())

class CreateAccountForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.CharField(label="email", widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    password_1 = forms.CharField(label="password-1", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password_2 = forms.CharField(label="password-2", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

class RecoverPasswordForm(forms.Form):
    email = forms.CharField(label="email", widget=forms.EmailInput())