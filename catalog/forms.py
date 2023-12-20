from django import forms
from catalog.models import Product


def check_forbidden_words(value):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    if value in forbidden_words:
        raise forms.ValidationError('введены недопустимые слова')

    return value


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        return check_forbidden_words(cleaned_data)

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        return check_forbidden_words(cleaned_data)
