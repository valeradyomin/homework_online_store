from django import forms
from catalog.models import Product, Version, Category


class StyleFormMiXin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active' and field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'


def check_forbidden_words(value):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    if value in forbidden_words:
        raise forms.ValidationError('введены недопустимые слова')

    return value


class ProductForm(StyleFormMiXin, forms.ModelForm):

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('owner', 'is_published',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        return check_forbidden_words(cleaned_data)

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        return check_forbidden_words(cleaned_data)


class VersionForm(StyleFormMiXin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')


class CategoryForm(StyleFormMiXin, forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
