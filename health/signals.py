from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from core.choices import CowProductionStatusChoices, CowPregnancyChoices
from core.models import Cow
from health.models import CullingRecord, QuarantineRecord, Disease, Recovery, Treatment


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

    if cow.availability_status != CowProductionStatusChoices.QUARANTINED:
        cow.availability_status = CowProductionStatusChoices.QUARANTINED
        cow.save()


@receiver(m2m_changed, sender=Disease.cows.through)
def set_disease_recovery_record(sender, instance, action, reverse, pk_set, **kwargs):
    """
    Signal handler for associating recovery records with cows after a Disease instance is linked.

    This signal is triggered when the Many-to-Many relationship between Disease and Cow instances is changed.
    Specifically, it responds to the 'post_add' action, occurring after linking Disease instances to cows.
    For each cow linked to the disease, it creates a Recovery record, indicating the diagnosis date.

    Args:
    - `sender`: The sender of the signal (Disease model's M2M relation with cows).
    - `instance`: The Disease instance being linked.
    - `action`: The type of action triggering the signal (e.g., 'post_add').
    - `reverse`: A boolean indicating whether the action is performed on the reverse side of the relation.
    - `pk_set`: A set of primary keys of the related objects being added.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that after linking Disease instances to cows, recovery records are created for each
        cow, indicating the diagnosis date.

    Example:
        To link a Disease instance to a set of cows:

        ```python
        disease_instance.cows.add(cow1, cow2, cow3)
        ```

        After this operation, the signal creates Recovery records for each cow.

    Note: This signal assumes that the 'date_reported' attribute of the Disease instance represents the diagnosis date.
    """
    if action == "post_add" and not reverse:
        for cow_id in pk_set:
            cow = Cow.objects.get(pk=cow_id)
            Recovery.objects.create(
                cow=cow, disease=instance, diagnosis_date=instance.date_reported
            )


@receiver(post_save, sender=Treatment)
def mark_cow_as_recovered(sender, instance, **kwargs):
    """
    Signal handler for updating the recovery date of a cow after a Treatment instance is saved.

    This signal is triggered after saving a Treatment instance. If the treatment is marked as 'completed' with a
    specified completion date, it updates the corresponding Recovery record's recovery_date attribute.

    Args:
    - `sender`: The sender of the signal (Treatment model).
    - `instance`: The Treatment instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that after a Treatment instance is marked as 'completed' with a completion date,
        the corresponding Recovery record's recovery date is updated.
    """
    if instance.completion_date:
        recovery = Recovery.objects.get(cow=instance.cow, disease=instance.disease)
        recovery.recovery_date = instance.completion_date
        recovery.save()
