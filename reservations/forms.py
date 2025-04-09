# reservations/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.forms import inlineformset_factory

from .models import Reservation, ReservationItem, MiscCharge
from customers.models import Customer


class ReservationForm(forms.ModelForm):
    """
    If 'new_customer' is checked, it creates a brand-new Customer
    using 'cust_first', 'cust_last', 'cust_email', 'cust_phone'.
    """
    new_customer = forms.BooleanField(required=False, label="Create new customer?")
    cust_first   = forms.CharField(max_length=100, required=False, label="First name")
    cust_last    = forms.CharField(max_length=100, required=False, label="Last name")
    cust_email   = forms.EmailField(required=False, label="Email")
    cust_phone   = forms.CharField(max_length=20, required=False, label="Phone")

    class Meta:
        model = Reservation
        fields = [
            "customer", "room", "check_in", "check_out",
            "number_of_guests", "deposit_amount", "status", "notes",
        ]
        widgets = {
            "check_in":  forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False  # <form> is in the template

        self.helper.layout = Layout(
            Row(
                Column("customer",     css_class="col-md-6"),
                Column("new_customer", css_class="col-md-6"),
            ),
            Row(
                Column("cust_first", css_class="col-md-3"),
                Column("cust_last",  css_class="col-md-3"),
                Column("cust_email", css_class="col-md-3"),
                Column("cust_phone", css_class="col-md-3"),
            ),
            Row(
                Column("room",       css_class="col-md-4"),
                Column("check_in",   css_class="col-md-4"),
                Column("check_out",  css_class="col-md-4"),
            ),
            Row(
                Column("number_of_guests", css_class="col-md-4"),
                Column("deposit_amount",   css_class="col-md-4"),
                Column("status",           css_class="col-md-4"),
            ),
            "notes"
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_customer"):
            # Minimal validation: require first & last name
            if not (cleaned_data.get("cust_first") and cleaned_data.get("cust_last")):
                raise forms.ValidationError(
                    "Provide first & last name for new customer."
                )
        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        if data.get("new_customer"):
            cust = Customer.objects.create(
                first_name = data["cust_first"],
                last_name  = data["cust_last"],
                email      = data["cust_email"],
                phone      = data["cust_phone"],
            )
            self.instance.customer = cust
        return super().save(commit)


# ───────── inline formsets ─────────
MenuItemFormSet = inlineformset_factory(
    Reservation, ReservationItem,
    fields      = ["menu_item", "quantity", "unit_price"],
    extra       = 1,
    can_delete  = True
)

MiscFormSet = inlineformset_factory(
    Reservation, MiscCharge,
    fields      = ["description", "amount"],
    extra       = 1,
    can_delete  = True
)
