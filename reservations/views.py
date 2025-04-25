# reservations/views.py
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reservation
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import ReservationForm, MenuItemFormSet, MiscFormSet
from django.shortcuts import get_object_or_404


class ReservationListView(ListView):
    model = Reservation
    template_name = "reservations/reservation_list.html"
    context_object_name = "reservations"
    paginate_by = 25

    def get_queryset(self):
        qs = Reservation.objects.select_related(
            "customer", "room", "room__category"
        ).order_by("-check_in")
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        if q:
            qs = qs.filter(
                Q(customer__first_name__icontains=q)
                | Q(customer__last_name__icontains=q)
                | Q(room__room_number__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reservation_status_choices"] = Reservation.STATUS_CHOICES
        return ctx


class ReservationCreateView(View):
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservations:reservation-list")

    def get(self, request, *args, **kwargs):
        # Initialize main form and inline formsets with prefixes matching your template JavaScript.
        form = ReservationForm()
        item_formset = MenuItemFormSet(prefix="reservationitem_set")
        misc_formset = MiscFormSet(prefix="misccharge_set")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "item_formset": item_formset,
                "misc_formset": misc_formset,
            },
        )

    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        # The prefixes must match those in the template & JavaScript code.
        item_formset = MenuItemFormSet(request.POST, prefix="reservationitem_set")
        misc_formset = MiscFormSet(request.POST, prefix="misccharge_set")

        if form.is_valid() and item_formset.is_valid() and misc_formset.is_valid():
            # Save the reservation form first.
            reservation = form.save(commit=False)
            reservation.save()

            # Attach the created reservation to each formset then save them.
            item_formset.instance = reservation
            item_formset.save()

            misc_formset.instance = reservation
            misc_formset.save()

            # If needed, add any messages or additional logic here.
            return redirect(self.success_url)

        # If not valid, render the form with errors.
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "item_formset": item_formset,
                "misc_formset": misc_formset,
            },
        )


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reservations/reservation_detail.html"
    context_object_name = "reservation"


class ReservationUpdateView(View):
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservations:reservation-list")

    def get(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=pk)
        form = ReservationForm(instance=reservation)

        item_formset = MenuItemFormSet(
            instance=reservation, prefix="reservationitem_set"
        )
        misc_formset = MiscFormSet(instance=reservation, prefix="misccharge_set")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "item_formset": item_formset,
                "misc_formset": misc_formset,
                "object": reservation,  # for {% if object %} in template
            },
        )

    def post(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=pk)
        form = ReservationForm(request.POST, instance=reservation)

        item_formset = MenuItemFormSet(
            request.POST, instance=reservation, prefix="reservationitem_set"
        )
        misc_formset = MiscFormSet(
            request.POST, instance=reservation, prefix="misccharge_set"
        )

        if form.is_valid() and item_formset.is_valid() and misc_formset.is_valid():
            form.save()
            item_formset.save()
            misc_formset.save()
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "item_formset": item_formset,
                "misc_formset": misc_formset,
                "object": reservation,
            },
        )


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = "reservations/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservations:reservation-list")
