# rooms/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django import forms
from .models import Room, RoomCategory


class RoomCategoryForm(forms.ModelForm):
    class Meta:
        model  = RoomCategory
        fields = ["name", "description", "base_price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("base_price", css_class="col-md-6"),
            ),
            Field("description"),
        )


class RoomForm(forms.ModelForm):
    class Meta:
        model  = Room
        fields = ["room_number", "category", "floor", "is_available"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("room_number", css_class="col-md-6"),
                Column("category",     css_class="col-md-6"),
            ),
            Row(
                Column("floor",        css_class="col-md-6"),
                Column("is_available", css_class="col-md-6"),
            ),
        )
