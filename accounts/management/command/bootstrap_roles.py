from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


#
#  Make sure a dummy permission “accounts | user | view_dashboard” exists
#
def ensure_view_dashboard_perm():
    ct = ContentType.objects.get_for_model(apps.get_model("accounts", "User"))
    Permission.objects.get_or_create(
        codename="view_dashboard",
        content_type=ct,
        defaults={"name": "Can view dashboard"},
    )
    
def ensure_permission_exists(codename, app_label, name):
    ct = ContentType.objects.get_for_model(apps.get_model(app_label, "Income"))
    Permission.objects.get_or_create(
        codename=codename,
        content_type=ct,
        defaults={"name": name},
    )

ROLE_PERMS: dict[str, dict[str, list[str]]] = {
    # 1 ───────────────────────────────────────────
    "general_manager": {
        "rooms": ["add_room", "change_room", "delete_room", "view_room"],
        "reservations": [
            "add_reservation",
            "change_reservation",
            "delete_reservation",
            "view_reservation",
        ],
        "billing": [
            "add_invoice",
            "change_invoice",
            "delete_invoice",
            "view_invoice",
            "add_payment",
            "view_payment",
        ],
        "reports": ["view_report"],
        "income": ["view_income", "add_income", "change_income"],
        "*": ["view_dashboard"],
    },
    # 2 ───────────────────────────────────────────
    "auditor": {
        "billing": ["view_invoice", "view_payment"],
        "rooms": ["view_room"],
        "reports": ["view_report"],
        "income": ["view_income"],
        "*": ["view_dashboard"],
    },
    # 3 ───────────────────────────────────────────
    "accountant": {
        "billing": ["view_invoice", "add_payment", "view_payment"],
        "reports": ["view_report"],
        "income": ["view_income", "add_income"],
        "*": ["view_dashboard"],
    },
    # 4 ───────────────────────────────────────────
    "hr": {
        "accounts": ["add_user", "change_user", "view_user"],
        "income": ["view_income", "add_income"],
        "*": ["view_dashboard"],
    },
    # 5 ───────────────────────────────────────────
    "admin_officer": {
        "accounts": ["view_user"],
        "reservations": ["view_reservation"],
        "*": ["view_dashboard"],
    },
    # 6 ───────────────────────────────────────────
    "supervisor": {
        "reservations": ["view_reservation", "change_reservation"],
        "rooms": ["view_room"],
        "*": ["view_dashboard"],
    },
    # 7 ───────────────────────────────────────────
    "chef": {
        "restaurant": ["view_menuitem", "add_kot", "view_kot"],
        "*": ["view_dashboard"],
    },
    # 8 ───────────────────────────────────────────
    "bar_waiter": {
        "restaurant": ["view_menuitem", "add_kot", "view_kot"],
        "*": ["view_dashboard"],
    },
    # 9 ───────────────────────────────────────────
    "room_service": {
        "restaurant": ["view_menuitem", "add_kot"],
        "reservations": ["view_reservation"],
        "*": ["view_dashboard"],
    },
    # 10 ──────────────────────────────────────────
    "restaurant_cashier": {
        "billing": ["add_invoice", "add_payment", "view_invoice", "view_payment"],
        "restaurant": ["view_kot"],
        "*": ["view_dashboard"],
    },
    # 11 ──────────────────────────────────────────
    "receptionist": {
        "reservations": ["add_reservation", "change_reservation", "view_reservation"],
        "rooms": ["view_room"],
        "customers": ["add_customer", "change_customer", "view_customer"],
        "*": ["view_dashboard"],
    },
}
class Command(BaseCommand):
    """
    Create / refresh one Django Group per staff role and attach the listed
    permissions.  Run:
        python manage.py bootstrap_roles
    """

    help = "Bootstrap role groups and permissions"

    def handle(self, *args, **kwargs):
        ensure_view_dashboard_perm()

        # Ensure all necessary permissions exist for Income
        ensure_permission_exists("view_income", "income", "Can view income")
        ensure_permission_exists("add_income", "income", "Can add income")
        ensure_permission_exists("change_income", "income", "Can change income")
        
        for role, app_perms in ROLE_PERMS.items():
            group, _ = Group.objects.get_or_create(name=role)
            group.permissions.clear()

            for app_label, codenames in app_perms.items():
                for codename in codenames:
                    if app_label == "*":
                        perm = Permission.objects.get(codename=codename)
                    else:
                        perm = Permission.objects.get(
                            codename=codename,
                            content_type__app_label=app_label,
                        )
                    group.permissions.add(perm)

            self.stdout.write(self.style.SUCCESS(f"✓  Group `{role}` updated"))

        self.stdout.write(self.style.SUCCESS("✔  All staff role groups refreshed"))


