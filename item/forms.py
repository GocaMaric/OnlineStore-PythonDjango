from django import forms
from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

def create_widget(field, widget_type, classes):
    return forms.fields_for_model(Item, fields=(field,))[field].formfield(widget=widget_type(attrs={'class': classes}))

class ItemFormMixin:
    def apply_custom_widgets(self):
        for field_name in self.Meta.fields:
            field = self.fields[field_name]
            widget_type = type(field.widget)
            field.widget = create_widget(field_name, widget_type, INPUT_CLASSES)

class NewItemForm(ItemFormMixin, forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_custom_widgets()

class EditItemForm(ItemFormMixin, forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_custom_widgets()

