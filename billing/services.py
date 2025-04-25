# billing/services.py
from decimal import Decimal
from django.db import transaction
from billing.models import Invoice, InvoiceLine
from reservations.models import Reservation


@transaction.atomic
def create_invoice_for_reservation(
    reservation: Reservation, vat_rate: Decimal = Decimal("0.075")
) -> Invoice:
    """
    Build (or rebuild) a COMBINED invoice for the given reservation.
    If an invoice already exists we delete its lines and recalc.
    """
    invoice, _ = Invoice.objects.get_or_create(
        reservation=reservation,
        defaults={
            "invoice_type": Invoice.COMBINED,
            "customer": reservation.customer,
        },
    )
    # wipe old lines if we’re regenerating
    invoice.lines.all().delete()

    # ---- Room charge ------------------------------------------------
    InvoiceLine.objects.create(
        invoice=invoice,
        description=f"Room {reservation.room.room_number} ({reservation.nights} nights)",
        quantity=1,
        unit_price=reservation.room_total,
        line_total=reservation.room_total,
    )

    # ---- Food items -------------------------------------------------
    for item in reservation.items.all():
        InvoiceLine.objects.create(
            invoice=invoice,
            description=item.menu_item.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.line_total,
        )

    # ---- Misc charges ----------------------------------------------
    for misc in reservation.misc.all():
        InvoiceLine.objects.create(
            invoice=invoice,
            description=misc.description,
            quantity=1,
            unit_price=misc.amount,
            line_total=misc.amount,
        )

    # Totals
    invoice.recalc(vat_rate=vat_rate)
    return invoice
