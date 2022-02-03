from django import forms
from django.core import validators
from captcha.fields import CaptchaField

from .models import Img


# Форма привязанная к модели, загружает по одному файлу.
class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение',
                           validators=[validators.FileExtensionValidator(
                               allowed_extensions=('gif', 'jpg', 'png'))],
                           error_messages={
                               'invalid_extension': 'Этот формат не поддерживается'},
                           allow_empty_file=False) # Файла с нулевым размером не допустимы.
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'


class CommentForm(forms.Form):
    pass


# Класс позволяет сохранять несколько файлом сразу.
class ImgNonModelForm(forms.Form):
    img = forms.ImageField(label='Изображение',
                           validators=[validators.FileExtensionValidator(
                               allowed_extensions=('gif', 'jpg', 'png'))],
                           error_messages={
                               'invalid_extension': 'Этот формат не поддерживается'},
                           widget=forms.widgets.ClearableFileInput(
                               attrs={'multiple':True})) # Позволяет загружать сразу несколько файлов.
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
