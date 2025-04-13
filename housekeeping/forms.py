from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from housekeeping.models import ComplaintTicket, Laundry

class LaundryForm(forms.ModelForm):
    class Meta:
        model = Laundry
        fields = [
            'reservation',
            'item_description',
            'cost',
            'total_items',
            'used_items',
            'returned_items',
            'status',
        ]
        widgets = {
            'item_description': forms.TextInput(attrs={'placeholder': 'Enter a description'}),
            'cost': forms.NumberInput(attrs={'step': '0.01'}),
            'total_items': forms.NumberInput(),
            'used_items': forms.NumberInput(),
            'returned_items': forms.NumberInput(),
            'status': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize Crispy Forms helper for consistent layout and styling.
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('reservation', css_class='col-md-6'),
                Column('status', css_class='col-md-6')
            ),
            Row(
                Column('item_description', css_class='col-md-12'),
            ),
            Row(
                Column('cost', css_class='col-md-4'),
                Column('total_items', css_class='col-md-4'),
                Column('used_items', css_class='col-md-4'),
            ),
            Row(
                Column('returned_items', css_class='col-md-12')
            ),
            Submit('submit', 'Save Laundry', css_class='btn btn-primary')
        )

class ComplaintTicketForm(forms.ModelForm):
    class Meta:
        model = ComplaintTicket
        fields = ['reservation', 'subject', 'description', 'resolved']
        widgets = {
            'reservation': forms.Select(attrs={'placeholder': 'Select Reservation'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description'}),
            'resolved': forms.CheckboxInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up Crispy Forms helper for a similar layout style as LaundryForm
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('reservation', css_class='col-md-6'),
                Column('resolved', css_class='col-md-6')
            ),
            Row(
                Column('subject', css_class='col-md-12'),
            ),
            Row(
                Column('description', css_class='col-md-12'),
            ),
            Submit('submit', 'Save Complaint', css_class='btn btn-primary')
        )
