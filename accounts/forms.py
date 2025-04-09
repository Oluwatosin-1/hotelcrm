# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column 
from .models import Staff
from .models import User    


class UserSignUpForm(UserCreationForm):
    """
    Custom sign-up form that includes the 'phone' field 
    plus the default fields from AbstractUser (username, email, password).
    """
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional placeholders or styling:
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Mobile / Phone'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})


class LoginForm(AuthenticationForm):
    """
    A login form that extends Django's AuthenticationForm,
    which already handles username + password validation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholder, ID, and class on the username field
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'id': 'username',
            'class': 'form-control'
        })
        # Set placeholder, ID, and class on the password field
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'id': 'password',
            'class': 'form-control pass-input'
        })
        
        
class StaffUserCreationForm(UserCreationForm):
    """
    One form that builds a User + Staff record.
    """
    # extra staff‑only fields
    role           = forms.ChoiceField(choices=Staff.ROLE_CHOICES, required=False)
    department     = forms.CharField(max_length=100, required=False)
    current_shift  = forms.ChoiceField(choices=Staff.SHIFT_CHOICES, required=False)
    staff_id       = forms.CharField(max_length=30, required=False,
                                     help_text="Optional employee/badge ID")

    can_add_room    = forms.BooleanField(required=False)
    can_edit_room   = forms.BooleanField(required=False)
    can_delete_room = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model  = User
        # UserCreationForm already contains username + password1 + password2
        fields = (
            "username", "first_name", "last_name", "email", "phone", "avatar",
            # password1, password2 come from parent
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("username",      css_class="col-md-6"),
                Column("email",         css_class="col-md-6"),
            ),
            Row(
                Column("first_name",    css_class="col-md-6"),
                Column("last_name",     css_class="col-md-6"),
            ),
            Row(
                Column("phone",         css_class="col-md-6"),
                Column("avatar",        css_class="col-md-6"),
            ),
            Row(
                Column("password1",     css_class="col-md-6"),
                Column("password2",     css_class="col-md-6"),
            ),
            # Staff‑specific section
            Row(
                Column("staff_id",      css_class="col-md-6"),
                Column("role",          css_class="col-md-6"),
            ),
            Row(
                Column("department",    css_class="col-md-6"),
                Column("current_shift", css_class="col-md-6"),
            ),
            Row(
                Column("can_add_room",    css_class="col-md-4"),
                Column("can_edit_room",   css_class="col-md-4"),
                Column("can_delete_room", css_class="col-md-4"),
            ),
        )

    def save(self, commit=True):
        """
        1. Create User (with hashed password).
        2. Create Staff linked to that user.
        """
        user = super().save(commit)
        staff = Staff.objects.create(
            user            = user,
            staff_id        = self.cleaned_data.get("staff_id") or "",
            role            = self.cleaned_data.get("role") or "",
            department      = self.cleaned_data.get("department") or "",
            current_shift   = self.cleaned_data.get("current_shift") or "",
            can_add_room    = self.cleaned_data.get("can_add_room"),
            can_edit_room   = self.cleaned_data.get("can_edit_room"),
            can_delete_room = self.cleaned_data.get("can_delete_room"),
        )
        return staff  # returning staff instance is OK


class StaffEditForm(forms.ModelForm):
    """
    Edit existing Staff + linked User profile fields.
    """

    # ---- User-side fields ----
    first_name = forms.CharField(max_length=150, required=False)
    last_name  = forms.CharField(max_length=150, required=False)
    email      = forms.EmailField(required=False)
    phone      = forms.CharField(max_length=20, required=False)
    avatar     = forms.ImageField(required=False)

    class Meta:
        model  = Staff
        fields = [
            # Staff fields
            "staff_id", "role", "department", "current_shift",
            "can_add_room", "can_edit_room", "can_delete_room",
            "is_active",
        ]

    # -----------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre‑populate user fields from the linked User object
        if self.instance and self.instance.pk:
            user = self.instance.user
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial  = user.last_name
            self.fields["email"].initial      = user.email
            self.fields["phone"].initial      = user.phone
            self.fields["avatar"].initial     = user.avatar

        # Crispy layout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col-md-6"),
                Column("last_name",  css_class="col-md-6"),
            ),
            Row(
                Column("email", css_class="col-md-6"),
                Column("phone", css_class="col-md-6"),
            ),
            Row(
                Column("avatar", css_class="col-md-12"),
            ),
            Row(
                Column("staff_id",   css_class="col-md-4"),
                Column("role",       css_class="col-md-4"),
                Column("department", css_class="col-md-4"),
            ),
            Row(
                Column("current_shift", css_class="col-md-4"),
                Column("is_active",     css_class="col-md-4"),
            ),
            Row(
                Column("can_add_room",    css_class="col-md-4"),
                Column("can_edit_room",   css_class="col-md-4"),
                Column("can_delete_room", css_class="col-md-4"),
            ),
        )

    # -----------------------------------------------------------------
    def save(self, commit=True):
        staff = super().save(commit=False)

        # Update linked User
        user = staff.user
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name  = self.cleaned_data.get("last_name", "")
        user.email      = self.cleaned_data.get("email", "")
        user.phone      = self.cleaned_data.get("phone", "")
        avatar          = self.cleaned_data.get("avatar")
        if avatar:
            user.avatar = avatar

        if commit:
            user.save()
            staff.save()

        return staff
