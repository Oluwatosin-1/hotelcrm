# accounts/signals.py  (very top)
from django.contrib.contenttypes.models import ContentType   # ←  add this
from django.contrib.auth.models        import Group, Permission
from django.db.models.signals          import post_save, post_migrate
from django.dispatch                   import receiver
from django.db                         import transaction
from accounts.models                   import Staff, User

# ────────────────────────────────────────────────────────────────
# 1.  Role → Permission matrix  (same list you use in bootstrap_roles)
# ----------------------------------------------------------------
ROLE_PERMS = {
    "general_manager": {
        "rooms":        ["add_room", "change_room", "delete_room", "view_room"],
        "reservations": ["add_reservation", "change_reservation", "delete_reservation", "view_reservation"],
        "billing":      ["add_invoice", "change_invoice", "delete_invoice", "view_invoice",
                         "add_payment", "view_payment"],
        "reports":      ["view_report"],
        "*":            ["view_dashboard"],
    },
    "auditor": {
        "billing": ["view_invoice", "view_payment"],
        "reports": ["view_report"],
        "*":       ["view_dashboard"],
    },
    "accountant": {
        "billing": ["view_invoice", "add_payment", "view_payment"],
        "*":       ["view_dashboard"],
    },
    "hr": {
        "accounts": ["add_user", "change_user", "view_user"],
        "*":        ["view_dashboard"],
    },
    "admin_officer": {
        "accounts": ["view_user"],
        "*":        ["view_dashboard"],
    },
    "supervisor": {
        "reservations": ["view_reservation", "change_reservation"],
        "*":            ["view_dashboard"],
    },
    "chef": {
        "restaurant": ["view_menuitem", "add_kot", "view_kot"],
        "*":          ["view_dashboard"],
    },
    "bar_waiter": {
        "restaurant": ["view_menuitem", "add_kot", "view_kot"],
        "*":          ["view_dashboard"],
    },
    "room_service": {
        "restaurant":  ["add_kot"],
        "reservations": ["view_reservation"],
        "*":            ["view_dashboard"],
    },
    "restaurant_cashier": {
        "billing": ["add_invoice", "add_payment", "view_invoice", "view_payment"],
        "*":       ["view_dashboard"],
    },
    "receptionist": {
        "reservations": ["add_reservation", "change_reservation", "view_reservation"],
        "rooms":        ["view_room"],
        "customers":    ["add_customer", "change_customer", "view_customer"],
        "*":            ["view_dashboard"],
    },
}

# ────────────────────────────────────────────────────────────────
# 2.  After *every* migrate, make sure groups & perms exist
# ----------------------------------------------------------------

@receiver(post_migrate)
@transaction.atomic
def create_role_groups(sender, **kwargs):
    # ----- ensure single custom perm on accounts.user -----
    ct = ContentType.objects.get_for_model(User)
    dashboard_perm, _ = Permission.objects.get_or_create(
        codename="view_dashboard",
        content_type=ct,
        defaults={"name": "Can view dashboard"},
    )

    # ----- build / refresh groups -----
    for role, app_perms in ROLE_PERMS.items():
        group, _ = Group.objects.get_or_create(name=role)
        group.permissions.clear()

        for app_label, codenames in app_perms.items():
            for codename in codenames:
                if app_label == "*":                   # only view_dashboard lives here
                    perm = dashboard_perm
                else:
                    try:
                        perm = Permission.objects.get(
                            codename=codename,
                            content_type__app_label=app_label,
                        )
                    except Permission.DoesNotExist:
                        # skip silently until the model is added / migrated
                        continue
                group.permissions.add(perm)
                
# ────────────────────────────────────────────────────────────────
# 3.  Whenever a Staff record is saved, sync its user’s group
# ----------------------------------------------------------------
@receiver(post_save, sender=Staff)
def sync_staff_group(sender, instance: Staff, **kwargs):
    user = instance.user
    user.groups.clear()

    if instance.role:
        grp = Group.objects.filter(name=instance.role).first()
        if grp:
            user.groups.add(grp)
