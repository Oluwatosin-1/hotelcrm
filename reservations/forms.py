from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML
from django import forms
from django.forms import inlineformset_factory

from .models import Reservation, ReservationItem, MiscCharge
from customers.models import Customer


class ReservationForm(forms.ModelForm):
    """
    When `new_customer` is checked, the extra customer fields are used to
    create a fresh Customer record and link it to the reservation.
    """
    # extra fields
    new_customer = forms.BooleanField(required=False, label="Create new customer?")
    cust_first   = forms.CharField(max_length=100, required=False, label="First name")
    cust_last    = forms.CharField(max_length=100, required=False, label="Last name")
    cust_email   = forms.EmailField(required=False, label="Email")
    cust_phone   = forms.CharField(max_length=20, required=False, label="Phone")

    class Meta:
        model = Reservation
        fields = [
            "customer", "new_customer",           # <- keep together
            "cust_first", "cust_last", "cust_email", "cust_phone",
            "room", "check_in", "check_out",
            "number_of_guests", "deposit_amount", "status",
            "notes",
        ]
        widgets = {
            "check_in":  forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "notes":     forms.Textarea(attrs={"rows": 3}),
        }

    # ─────────────────────────────────────────────────────────────
    # Crispy layout
    # ─────────────────────────────────────────────────────────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False  # <form> tag lives in template
        self.fields["customer"].required = False
        self.helper.layout = Layout(
            Row(
                Column("customer",     css_class="col-md-6"),
                Column("new_customer", css_class="col-md-6"),
            ),

            # --- new‑customer block (hidden by default) -------------
            Div(
                HTML("<hr><h5 class='fw-semibold mb-3'>New Customer Details</h5>"),
                Row(
                    Column("cust_first",  css_class="col-md-3"),
                    Column("cust_last",   css_class="col-md-3"),
                    Column("cust_email",  css_class="col-md-3"),
                    Column("cust_phone",  css_class="col-md-3"),
                ),
                css_class="d-none",      # toggled by JS
                css_id="new-customer-fields",
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
            "notes",
        )

    # ─────────────────────────────────────────────────────────────
    # Validation & save hook
    # ─────────────────────────────────────────────────────────────
    def clean(self):
        cd = super().clean()

        new_cust = cd.get("new_customer")
        chosen   = cd.get("customer")

        # ➋ Must EITHER tick the box and give names OR pick a customer
        if not new_cust and not chosen:
            raise forms.ValidationError("Select an existing customer or tick “Create new customer?”.")
        if new_cust:
            if not (cd.get("cust_first") and cd.get("cust_last")):
                raise forms.ValidationError("First & last name are required for a new customer.")
        return cd


    def save(self, commit=True):
        data = self.cleaned_data
        if data.get("new_customer"):
            customer = Customer.objects.create(
                first_name=data["cust_first"],
                last_name=data["cust_last"],
                email=data["cust_email"],
                phone=data["cust_phone"],
            )
            self.instance.customer = customer
        return super().save(commit=commit)
    


# ───────── inline formsets ─────────
MenuItemFormSet = inlineformset_factory(
    Reservation, ReservationItem,
    fields=["menu_item", "quantity", "unit_price"],
    extra=1,
    can_delete=True,
)

MiscFormSet = inlineformset_factory(
    Reservation, MiscCharge,
    fields=["description", "amount"],
    extra=1,
    can_delete=True,
)
