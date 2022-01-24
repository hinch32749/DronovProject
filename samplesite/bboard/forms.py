from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet, modelformset_factory

from .models import Bb, Rubric


# class BbForm(forms.ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric', 'kind')


class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{3,}$')],
                            error_messages={'invalid': 'Слишком короткое название товара'})
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), empty_label=None,
                                    label='Рубрика',
                                    help_text='Не забудьте задать рубрику!',
                                    widget=forms.widgets.RadioSelect(attrs={'size': 6}))

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Цена не может быть отрицательной!')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'kind')
        labels = {'title': 'Название товара'}


# Виджет для выбора года, месяца и числа из трех списков
#     date = forms.DateField(widget=forms.widgets.SelectDateWidget(
#             empty_label=('Выберите год', 'Выберите месяц', 'Выберите число')))

# Валидация поля "price", не работает с Классом редактирования т.к. нет cleaned_data
#     def clean_price(self):
#         val = self.cleaned_data['price']
#         if val < 0:
#             raise ValidationError("Цена на товар не может быть отрицательной!")

# ========================================================================================================

class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms
                 if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) or ('Мебель' not in names):
            raise ValidationError('Добавьте рубрики недвижимости, транспорта и мебели')


# Форма не связанная с моделью для поиска Рубрик.
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')
