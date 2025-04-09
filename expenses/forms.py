from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Expense, ExpenseCategory, ExpenseSubCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'description', 'amount', 'date',
            'category', 'subcategory',
            'payment_method', 'notes'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy Forms helper for layout customization
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('description', css_class='col-md-6'),
                Column('amount', css_class='col-md-6')
            ),
            Row(
                Column('date', css_class='col-md-6'),
                Column('payment_method', css_class='col-md-6'),
            ),
            Row(
                Column('category', css_class='col-md-6'),
                Column('subcategory', css_class='col-md-6'),
            ),
            'notes',
            Submit('submit', 'Save Expense', css_class='btn btn-primary mt-3')
        )

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'description',
            Submit('submit', 'Save Category', css_class='btn btn-primary mt-3')
        )

class ExpenseSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseSubCategory
        fields = ['category', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='col-md-6'),
                Column('name', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Subcategory', css_class='btn btn-primary mt-3')
        )
