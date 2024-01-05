from django.db.models.signals import post_save, pre_delete
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from core.models import Cow, CowInventory

@receiver(post_save, sender=Cow)
def update_cow_inventory_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to update the CowInventory on cow save.

    Args:
    - `sender` (Model): The model class that sent the signal.
    - `instance` (Cow): The instance of the Cow model that triggered the signal.
    - `created` (bool): Indicates whether the instance was created or updated.
    - `kwargs` (dict): Additional keyword arguments.

    Notes:
    - This signal handler updates the CowInventory counts based on cow creation or update.
    - It is automatically triggered after a Cow model instance is saved.
    """
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        cow_inventory = CowInventory.objects.create(
            pk=1,
            total_number_of_cows=0,
            number_of_male_cows=0,
            number_of_female_cows=0,
            number_of_sold_cows=0,
            number_of_dead_cows=0
        )

    if instance.is_bought and instance.availability_status == "ALIVE":
        cow_inventory.total_number_of_cows += 1

        if instance.gender == 'Male':
            cow_inventory.number_of_male_cows += 1
        elif instance.gender == 'Female':
            cow_inventory.number_of_female_cows += 1

    elif not instance.is_bought and instance.availability_status == 'ALIVE':
        cow_inventory.total_number_of_cows += 1

        if instance.gender == 'Male':
            cow_inventory.number_of_male_cows += 1
        elif instance.gender == 'Female':
            cow_inventory.number_of_female_cows += 1

    elif instance.availability_status == "SOLD":
        cow_inventory.number_of_sold_cows += 1
        cow_inventory.total_number_of_cows -= 1

        if instance.gender == 'Male':
            cow_inventory.number_of_male_cows -= 1
        elif instance.gender == 'Female':
            cow_inventory.number_of_female_cows -= 1

    elif instance.availability_status == "DEAD":
        cow_inventory.number_of_dead_cows += 1
        cow_inventory.total_number_of_cows -= 1

        if instance.gender == 'Male':
            cow_inventory.number_of_male_cows -= 1
        elif instance.gender == 'Female':
            cow_inventory.number_of_female_cows -= 1

    cow_inventory.save()

@receiver(pre_delete, sender=Cow)
def update_cow_inventory_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the CowInventory on cow deletion.

    Args:
    - `sender` (Model): The model class that sent the signal.
    - `instance` (Cow): The instance of the Cow model that triggered the signal.
    - `kwargs` (dict): Additional keyword arguments.

    Notes:
    - This signal handler updates the CowInventory counts based on cow deletion.
    - It is automatically triggered before a Cow model instance is deleted.
    """
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        # Handle the case where CowInventory does not exist (optional)
        return

    cow_inventory.total_number_of_cows -= 1

    if instance.gender == 'Male':
        cow_inventory.number_of_male_cows -= 1
    elif instance.gender == 'Female':
        cow_inventory.number_of_female_cows -= 1

    cow_inventory.save()
