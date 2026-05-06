from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Document, PageLink

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "description", "category", "file"]


class PageLinkForm(forms.ModelForm):
    class Meta:
        model = PageLink
        fields = ["title", "url", "description"]

    def clean_url(self):
        url = self.cleaned_data["url"].strip()
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        return url
