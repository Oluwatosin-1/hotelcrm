# billing/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from billing.models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        # Exclude computed fields: sub_total, taxes, total_amount
        fields = [
            'invoice_date',
            'invoice_type',
            'reservation',
            'kot',
            'customer',
            'is_paid',
        ]
        widgets = {
            'invoice_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'invoice_date': 'Invoice Date & Time',
            'invoice_type': 'Invoice Type',
            'reservation': 'Reservation',
            'kot': 'KOT (if applicable)',
            'customer': 'Customer',
            'is_paid': 'Mark as Paid',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('invoice_date', css_class='col-md-4'),
                Column('invoice_type', css_class='col-md-4'),
                Column('is_paid', css_class='col-md-4'),
            ),
            Row(
                Column('reservation', css_class='col-md-4'),
                Column('kot', css_class='col-md-4'),
                Column('customer', css_class='col-md-4'),
            ),
            HTML("<hr>"),
            Submit("submit", "Save Invoice", css_class="btn btn-primary")
        )
