from django.utils.functional import SimpleLazyObject


def clock_status(request):
    def _open():
        if request.user.is_authenticated:
            # assumes your TimeEntry has related_name='time_entries'
            return request.user.time_entries.filter(clock_out__isnull=True).exists()
        return False

    # wrap in lazy so it only hits the DB if template actually uses it
    return {"is_clocked_in": SimpleLazyObject(_open)}
