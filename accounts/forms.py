# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div, Submit, HTML
from django.contrib.contenttypes.models import ContentType
from accounts.models import TimeEntry, User, Staff 
from django.contrib.auth.models import Group, Permission 
from django.contrib.auth.forms import UserChangeForm 
class GroupPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type').all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Group Permissions",
    )

    class Meta:
        model = Group
        fields = ["permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Group by content type for visual clarity
        grouped = {}
        for perm in self.fields["permissions"].queryset:
            app = perm.content_type.app_label.title()
            grouped.setdefault(app, []).append((perm.id, perm.name))

        self.fields["permissions"].choices = [
            (app_label, perms) for app_label, perms in grouped.items()
        ]

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("permissions", css_class="form-group"),
        )

class UserPermissionForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="User-Specific Permissions",
    )

    class Meta:
        model = User
        fields = ["user_permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grouped = {}
        for perm in self.fields["user_permissions"].queryset:
            app = perm.content_type.app_label.title()
            grouped.setdefault(app, []).append((perm.id, perm.name))

        self.fields["user_permissions"].choices = [
            (app_label, perms) for app_label, perms in grouped.items()
        ]

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("user_permissions", css_class="form-group"),
        )

class UserProfileForm(UserChangeForm):
    # Personal fields (we override some defaults for styling and placeholder)
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, label="Phone", required=False)
    avatar = forms.ImageField(label="Avatar", required=False)
    
    # Staff-related fields (will only be editable by admin/HR/super_admin)
    role = forms.ChoiceField(choices=Staff.ROLE_CHOICES, label="Role", required=False)
    department = forms.CharField(max_length=100, label="Department", required=False)
    current_shift = forms.ChoiceField(choices=Staff.SHIFT_CHOICES, label="Shift", required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        # Expect the view to pass in the currently logged-in user as 'current_user'
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        
        # Setup Crispy Forms helper for styling
        self.helper = FormHelper()
        self.helper.form_method = "post"
        
        # Decide if the staff fields should be editable.
        # For example, only allow if current_user is superuser or has a specific permission.
        if current_user and (current_user.is_superuser or current_user.has_perm('accounts.change_role')):
            # Staff fields will be available
            staff_fields_layout = Layout(
                Row(
                    Column('role', css_class='col-md-4'),
                    Column('department', css_class='col-md-4'),
                    Column('current_shift', css_class='col-md-4'),
                )
            )
        else:
            # Remove staff-related fields from the form
            self.fields.pop('role', None)
            self.fields.pop('department', None)
            self.fields.pop('current_shift', None)
            staff_fields_layout = None
        
        # Build full layout
        layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('avatar', css_class='col-md-6'),
            ),
        )
        
        if staff_fields_layout:
            layout.append(HTML("<hr><h5 class='mt-3'>Staff Details</h5>"))
            layout.append(staff_fields_layout)
            
        layout.append(Submit('submit', 'Save Changes', css_class='btn btn-primary mt-3'))
        self.helper.layout = layout

    def save(self, commit=True):
        # Save the User instance first.
        user = super().save(commit=False)
        if commit:
            user.save()

        # Save staff-related fields if available and if the user has a staff profile
        if hasattr(user, 'staff_profile'):
            staff = user.staff_profile
            if 'role' in self.cleaned_data:  # field exists only if user is allowed to edit
                staff.role = self.cleaned_data.get('role') or staff.role
            if 'department' in self.cleaned_data:
                staff.department = self.cleaned_data.get('department') or staff.department
            if 'current_shift' in self.cleaned_data:
                staff.current_shift = self.cleaned_data.get('current_shift') or staff.current_shift
            staff.save()
        return user
# ──────────────────────────────────────────────────────────────
# 1.  PUBLIC USER SIGN‑UP  (optional)
# ----------------------------------------------------------------
class UserSignUpForm(UserCreationForm):
    """Plain user registration (not staff)."""
    class Meta:
        model  = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None


# ──────────────────────────────────────────────────────────────
# 2.  LOGIN
# ----------------------------------------------------------------
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "class": "form-control"}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Password", "class": "form-control pass-input"}
        )


# ──────────────────────────────────────────────────────────────
# 3.  SELF‑SERVICE STAFF APPLICATION  →  status=PENDING
# ----------------------------------------------------------------
class StaffSignupForm(UserCreationForm):
    role        = forms.ChoiceField(choices=Staff.ROLE_CHOICES, label="Desired role")
    department  = forms.CharField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    # Crispy layout
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("username", css_class="col-md-6"),
                Column("email",    css_class="col-md-6")),
            Row(Column("first_name", css_class="col-md-6"),
                Column("last_name",  css_class="col-md-6")),
            Row(Column("phone", css_class="col-md-6")),
            Row(Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6")),
            Row(Column("role", css_class="col-md-6"),
                Column("department", css_class="col-md-6")),
        )

    # Create user + pending staff
    def save(self, commit=True):
        user = super().save(commit)
        Staff.objects.create(
            user       = user,
            role       = self.cleaned_data["role"],
            department = self.cleaned_data.get("department", ""),
            status     = Staff.PENDING,
        )
        return user


# ──────────────────────────────────────────────────────────────
# 4.  HR / MANAGER  –  CREATE APPROVED STAFF IN ONE GO
# ----------------------------------------------------------------
class StaffUserCreationForm(UserCreationForm):
    # Staff‑specific extras
    role           = forms.ChoiceField(choices=Staff.ROLE_CHOICES)
    department     = forms.CharField(max_length=100, required=False)
    current_shift  = forms.ChoiceField(choices=Staff.SHIFT_CHOICES, required=False)
    staff_id       = forms.CharField(max_length=30, required=False) 

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = (
            "username", "first_name", "last_name", "email", "phone", "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("username", css_class="col-md-6"),
                Column("email",    css_class="col-md-6")),
            Row(Column("first_name", css_class="col-md-6"),
                Column("last_name",  css_class="col-md-6")),
            Row(Column("phone",  css_class="col-md-6"),
                Column("avatar", css_class="col-md-6")),
            Row(Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6")),
            Row(Column("staff_id", css_class="col-md-6"),
                Column("role",     css_class="col-md-6")),
            Row(Column("department",    css_class="col-md-6"),
                Column("current_shift", css_class="col-md-6")), 
        )

    def save(self, commit=True):
        user = super().save(commit)
        Staff.objects.create(
            user            = user,
            staff_id        = self.cleaned_data.get("staff_id") or "",
            role            = self.cleaned_data["role"],
            department      = self.cleaned_data.get("department", ""),
            current_shift   = self.cleaned_data.get("current_shift", ""), 
            status          = Staff.APPROVED,          # ← immediately active
        )
        return user


# ──────────────────────────────────────────────────────────────
# 5.  EDIT EXISTING STAFF  (+ linked User)
# ----------------------------------------------------------------
class StaffEditForm(forms.ModelForm):
    # user‑side fields
    first_name = forms.CharField(max_length=150, required=False)
    last_name  = forms.CharField(max_length=150, required=False)
    email      = forms.EmailField(required=False)
    phone      = forms.CharField(max_length=20,  required=False)
    avatar     = forms.ImageField(required=False)

    class Meta:
        model  = Staff
        fields = [
            "staff_id", "role", "department", "current_shift", 
            "is_active", "status",
        ]

    # ----- init -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            u = self.instance.user
            self.initial.update(
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,
                phone=u.phone,
                avatar=u.avatar,
            )

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("first_name", css_class="col-md-6"),
                Column("last_name",  css_class="col-md-6")),
            Row(Column("email", css_class="col-md-6"),
                Column("phone", css_class="col-md-6")),
            Field("avatar"),
            Row(Column("staff_id", css_class="col-md-4"),
                Column("role",     css_class="col-md-4"),
                Column("department", css_class="col-md-4")),
            Row(Column("current_shift", css_class="col-md-4"),
                Column("status",        css_class="col-md-4"),
                Column("is_active",     css_class="col-md-4")), 
        )

    # ----- save -----
    def save(self, commit=True):
        staff = super().save(commit=False)
        user  = staff.user
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name  = self.cleaned_data.get("last_name", "")
        user.email      = self.cleaned_data.get("email", "")
        user.phone      = self.cleaned_data.get("phone", "")
        if avatar := self.cleaned_data.get("avatar"):
            user.avatar = avatar

        if commit:
            user.save()
            staff.save()
        return staff

class StaffApprovalForm(forms.ModelForm):
    """HR / Manager can flip status + set granular flags."""
    class Meta:
        model  = Staff
        fields = ["status", "approved_by", 
                  "is_active"]
 
class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ["clock_in", "clock_out", "notes"]
        widgets = {
            "clock_in":  forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clock_out": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes":     forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("clock_in", css_class="col-md-6"),
                Column("clock_out", css_class="col-md-6"),
            ),
            "notes",
            Submit("submit", "Save", css_class="btn btn-primary mt-3")
        )

class TimeEntryAdminForm(forms.ModelForm):
    """
    Used by managers/supervisors to edit any entry.
    Regular employees never see this.
    """
    class Meta:
        model   = TimeEntry
        fields  = ["user", "clock_in", "clock_out", "notes"]
        widgets = {
            "clock_in":  forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clock_out": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(Column("user",       css_class="col-md-4"),
                Column("clock_in",   css_class="col-md-4"),
                Column("clock_out",  css_class="col-md-4")),
            "notes",
            Submit("submit", "Save", css_class="btn btn-primary mt-3")
        )