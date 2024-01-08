from django.db import models


class CowInventory(models.Model):
    """
    Represents the cow inventory of the dairy farm.

    Attributes:
    - `total_number_of_cows` (PositiveIntegerField): Total number of cows in the inventory.
    - `number_of_male_cows` (PositiveIntegerField): Number of male cows in the inventory.
    - `number_of_female_cows` (PositiveIntegerField): Number of female cows in the inventory.
    - `number_of_sold_cows` (PositiveIntegerField): Number of cows that have been sold.
    - `number_of_dead_cows` (PositiveIntegerField): Number of cows that have died.
    - `last_update` (DateTimeField): Date and time of the last update to the inventory.

    Note:
    This model is designed to automatically update the counts based on changes to the Cow model using a signal handler.
    """

    total_number_of_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_male_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_female_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_sold_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_dead_cows = models.PositiveIntegerField(default=0, editable=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Cow Inventory - Total: {self.total_number_of_cows}, Male: {self.number_of_male_cows}, "
            f"Female: {self.number_of_female_cows}, Sold: {self.number_of_sold_cows}, "
            f"Dead: {self.number_of_dead_cows}, Last Update: {self.last_update}"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        CowInventoryUpdateHistory.objects.create(
            number_of_cows=self.total_number_of_cows
        )


class CowInventoryUpdateHistory(models.Model):
    """
    Represents the historical changes to the cow inventory over time.
    Fields:
    - `number_of_cows` (PositiveIntegerField): Total number of cows in the inventory at the time of the update.
    - `date_updated` (DateField): Date of the cow inventory update.
    Note:
    This model logs historical changes to the cow inventory, capturing the total number of cows and the date of each update.
    """

    number_of_cows = models.PositiveIntegerField(default=0, editable=False)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Cow Inventory History - Total Cows: {self.number_of_cows}, Date: {self.date_updated}"
