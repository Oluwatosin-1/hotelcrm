from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from crispy_forms.bootstrap import FormActions
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "first_name", "last_name",
            "gender", "date_of_birth",
            "email", "phone",
            "address",
            "id_card_type", "id_card_number",
            "notes",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Optional: add placeholders
        self.fields["first_name"].widget.attrs["placeholder"] = "First name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last name"
        self.fields["email"].widget.attrs["placeholder"] = "example@email.com"
        self.fields["phone"].widget.attrs["placeholder"] = "+234‑801‑234‑5678"

        # Crispy Forms helper & layout
        self.helper = FormHelper()
        self.helper.form_tag = False  # <form> will be in the template
        self.helper.label_class = "form-label fw-semibold"
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col-md-6"),
                Column("last_name",  css_class="col-md-6")
            ),
            Row(
                Column("gender",        css_class="col-md-6"),
                Column("date_of_birth", css_class="col-md-6")
            ),
            Row(
                Column("email", css_class="col-md-6"),
                Column("phone", css_class="col-md-6")
            ),
            Field("address"),
            Row(
                Column("id_card_type",   css_class="col-md-6"),
                Column("id_card_number", css_class="col-md-6")
            ),
            Field("notes")
        )
