from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from core.models import Cow, CowInventory

'''@receiver(post_save, sender=Cow)
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
        cow_inventory = CowInventory.objects.create()

    cow_inventory.total_number_of_cows = Cow.objects.filter(
        availability_status="Alive"
    ).count()
    cow_inventory.number_of_male_cows = Cow.objects.filter(
        availability_status="Alive", gender="Male"
    ).count()
    cow_inventory.number_of_female_cows = Cow.objects.filter(
        availability_status="Alive", gender="Female"
    ).count()
    cow_inventory.number_of_sold_cows = Cow.objects.filter(
        availability_status="Sold"
    ).count()
    cow_inventory.number_of_dead_cows = Cow.objects.filter(
        availability_status="Dead"
    ).count()

    cow_inventory.save()

@receiver(post_delete, sender=Cow)
def update_cow_inventory_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the CowInventory on cow delete.

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
        cow_inventory = CowInventory.objects.create()

    cow_inventory.total_number_of_cows = Cow.objects.filter(
        availability_status="Alive"
    ).count()
    cow_inventory.number_of_male_cows = Cow.objects.filter(
        availability_status="Alive", gender="Male"
    ).count()
    cow_inventory.number_of_female_cows = Cow.objects.filter(
        availability_status="Alive", gender="Female"
    ).count()
    cow_inventory.number_of_sold_cows = Cow.objects.filter(
        availability_status="Sold"
    ).count()
    cow_inventory.number_of_dead_cows = Cow.objects.filter(
        availability_status="Dead"
    ).count()

    cow_inventory.save()
'''
def update_cow_inventory(cow_inventory):
    cow_inventory.total_number_of_cows = Cow.objects.filter(
        availability_status="Alive"
    ).count()
    cow_inventory.number_of_male_cows = Cow.objects.filter(
        availability_status="Alive", gender="Male"
    ).count()
    cow_inventory.number_of_female_cows = Cow.objects.filter(
        availability_status="Alive", gender="Female"
    ).count()
    cow_inventory.number_of_sold_cows = Cow.objects.filter(
        availability_status="Sold"
    ).count()
    cow_inventory.number_of_dead_cows = Cow.objects.filter(
        availability_status="Dead"
    ).count()

    cow_inventory.save()

@receiver(post_save, sender=Cow)
def update_cow_inventory_on_save(sender, instance, created, **kwargs):
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        cow_inventory = CowInventory.objects.create()

    update_cow_inventory(cow_inventory)

@receiver(post_delete, sender=Cow)
def update_cow_inventory_on_delete(sender, instance, **kwargs):
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        cow_inventory = CowInventory.objects.create()

    update_cow_inventory(cow_inventory)
