from django.db.models.signals import post_save
from django.dispatch import receiver

from core.choices import CowProductionStatusChoices, CowPregnancyChoices, CowAvailabilityChoices
from health.models import CullingRecord, QuarantineRecord


@receiver(post_save, sender=CullingRecord)
def set_cow_production_status_to_culled(sender, instance, **kwargs):
    """
    Signal handler for setting the production status of a cow to 'CULLED' after culling.

    This signal is triggered after saving a CullingRecord instance. It updates the production
    status of the associated cow to 'CULLED' and sets the pregnancy status to 'UNAVAILABLE'.

    Args:
    - `sender`: The sender of the signal (CullingRecord model in this case).
    - `instance`: The CullingRecord instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that after a cow is culled, its production status is updated to 'CULLED'
        and its pregnancy status is set to 'UNAVAILABLE'.
    """
    cow = instance.cow

    if cow.current_production_status != CowProductionStatusChoices.CULLED:
        cow.current_production_status = CowProductionStatusChoices.CULLED
        cow.current_pregnancy_status = CowPregnancyChoices.UNAVAILABLE
        cow.save()

@receiver(post_save, sender=QuarantineRecord)
def set_cow_availability_to_quarantined(sender, instance, **kwargs):
    """
    Signal handler for setting the availability status of a cow to 'QUARANTINED' after quarantine.

    This signal is triggered after saving a QuarantineRecord instance. It updates the availability
    status of the associated cow to 'QUARANTINED'.

    Args:
    - `sender`: The sender of the signal (QuarantineRecord model in this case).
    - `instance`: The QuarantineRecord instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that after a cow is quarantined, its availability status is updated to 'QUARANTINED'.
    """
    cow = instance.cow

    if cow.availability_status != CowAvailabilityChoices.QUARANTINED:
        cow.availability_status = CowAvailabilityChoices.QUARANTINED
        cow.save()
