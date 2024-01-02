from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Cow
from production.models import Lactation
from reproduction.choices import PregnancyOutcomeChoices
from reproduction.models import Pregnancy, Insemination


@receiver(post_save, sender=Pregnancy)
def create_lactation(sender, instance, **kwargs):
    """
    Signal handler for creating a new lactation record after a pregnancy record is saved.

    This signal is triggered after saving a Pregnancy instance. It checks if the pregnancy
    resulted in a live birth or stillbirth. If true, it marks the cow as recently calved
    and creates a new lactation record based on the date of calving.

    Args:
    - `sender`: The sender of the signal (Pregnancy model in this case).
    - `instance`: The Pregnancy instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that a new lactation record is created for the cow after a successful calving.
        It also marks the cow as recently calved.
    """
    if not instance.date_of_calving and instance.pregnancy_outcome not in [
        PregnancyOutcomeChoices.LIVE,
        PregnancyOutcomeChoices.STILLBORN,
    ]:
        return

    Cow.objects.mark_a_recently_calved_cow(instance.cow)

    try:
        previous_lactation = Lactation.objects.filter(cow=instance.cow).latest()

        if previous_lactation and not previous_lactation.end_date:
            previous_lactation.end_date = instance.date_of_calving - timedelta(days=1)
            previous_lactation.save()

            Lactation.objects.create(
                start_date=instance.date_of_calving,
                cow=instance.cow,
                pregnancy=instance,
                lactation_number=previous_lactation.lactation_number + 1,
            )
    except Lactation.DoesNotExist:
        Lactation.objects.create(
            start_date=instance.date_of_calving, cow=instance.cow, pregnancy=instance
        )


@receiver(post_save, sender=Insemination)
def create_pregnancy_from_successful_insemination(sender, instance, **kwargs):
    """
    Signal handler for creating a new pregnancy record after a successful insemination.

    This signal is triggered after saving an Insemination instance. If the insemination
    was successful and there is no existing pregnancy record for the cow, it creates a
    new pregnancy record associated with the cow and the date of insemination.

    Args:
    - `sender`: The sender of the signal (Insemination model in this case).
    - `instance`: The Insemination instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that a new pregnancy record is created after a successful insemination,
        and the cow is associated with the pregnancy based on the date of insemination.
    """
    if instance.success and not instance.pregnancy:
        pregnancy = Pregnancy.objects.create(
            cow=instance.cow, start_date=instance.date_of_insemination.date()
        )
        pregnancy.save()

        instance.pregnancy = pregnancy
        instance.save()
