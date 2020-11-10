from django import forms


class Searchform(forms.Form):
    query = forms.CharField()


class Loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
