# reports/forms.py
from django import forms
from .models import Report


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
