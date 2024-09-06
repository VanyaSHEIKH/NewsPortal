from django import forms
from django.core.exceptions import ValidationError

from .models import *


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=25)
    text = forms.CharField(max_length=200)

    class Meta:
        model = Post
        fields = [
            'author',
            'post_type',
            'rating',
            'title',
            'category',
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get("post_text")
        title = cleaned_data.get("title")

        if title == post_text:
            raise ValidationError(
                "Значение Title не должно быть таким же, как и Text."
            )

        return cleaned_data


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['category']