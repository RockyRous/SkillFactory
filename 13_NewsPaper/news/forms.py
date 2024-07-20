from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class NewsForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',
        ]
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категории'
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")
        if name == description:
            raise ValidationError(
                "Текст не должен быть идентичным названию."
            )
        if description is not None and len(description) < 20:
            raise ValidationError({
                "description": "Текст не может быть менее 20 символов."
            })
        return cleaned_data
