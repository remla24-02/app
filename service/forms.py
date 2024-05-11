from django import forms


class URLDetectForm(forms.Form):
    url = forms.CharField()
