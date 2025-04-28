# reports/forms.py
from django import forms
from .models import Report 
from .models import Income, IncomeCategory 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit 

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description', 'amount', 'category', 'payment_method', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Restrict 'category' field to only existing categories
        self.fields['category'].queryset = IncomeCategory.objects.all()

        # Crispy Forms helper for layout customization
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('description', css_class='col-md-6'),
                Column('amount', css_class='col-md-6'),
            ),
            Row(
                Column('category', css_class='col-md-6'),
                Column('payment_method', css_class='col-md-6'),
            ),
            'notes',  # 'notes' field doesn't need to be divided into columns since it's a Textarea
            Submit('submit', 'Save Income', css_class='btn btn-primary mt-3')
        )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Income amount must be greater than 0.")
        return amount

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 5:
            raise forms.ValidationError("Description must be at least 5 characters long.")
        return description

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["name", "description", "report_file"]

    # Example of custom validation
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 5:
            raise forms.ValidationError(
                "The report name must be at least 5 characters long."
            )
        return name
