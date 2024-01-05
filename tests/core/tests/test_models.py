import pytest
from django.core.exceptions import ValidationError

from core.choices import (
    CowBreedChoices,
    CowAvailabilityChoices,
    CowPregnancyChoices,
    CowCategoryChoices,
    CowProductionStatusChoices,
)
from core.models import CowBreed, Cow, CowInventory
from users.choices import SexChoices
from core.utils import todays_date
from datetime import timedelta

# @pytest.mark.django_db
# class TestCowBreedModel:
#     def test_save_breed_with_valid_name(self):
#         breed = CowBreed.objects.create(name=CowBreedChoices.JERSEY)
#         assert breed.name == CowBreedChoices.JERSEY

#     def test_create_breed_with_invalid_name(self):
#         with pytest.raises(ValidationError) as err:
#             CowBreed.objects.create(name="unknown_breed")
#         assert err.value.code == 'invalid_cow_breed'

#     def test_create_breed_with_duplicate_name(self):
#         # Create a breed with a valid name first
#         CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)

#         # Attempt to create another breed with the same name, should raise ValidationError
#         with pytest.raises(ValidationError) as err:
#             CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
#         assert err.value.code == 'duplicate_cow_breed'


@pytest.mark.django_db
class TestCowInventoryModel:
    @pytest.fixture(autouse=True)
    def setup(self, setup_cows):
        self.cow_data = setup_cows

    def test_cow_inventory_creation(self):
        Cow.objects.create(**self.cow_data)
        assert CowInventory.objects.all().count() == 1
        print(CowInventory.objects.all())

    # def test_cow_inventory_creation(self):
    #     cow_inventory = CowInventory.objects.create(
    #         pk = 1,
    #         total_number_of_cows=10,
    #         number_of_male_cows=5,
    #         number_of_female_cows=5,
    #         number_of_sold_cows=2,
    #         number_of_dead_cows=1
    #     )
    #     assert cow_inventory.pk is not None

    # def test_cow_inventory_update_on_cow_creation(initial_cow_inventory):
    #     # Create a new cow
    #     cow = Cow.objects.create(
    #         name="General Cow",
    #         breed=CowBreed.objects.create(name=CowBreedChoices.JERSEY),
    #         date_of_birth=todays_date - timedelta(days=370),
    #         gender=SexChoices.FEMALE,
    #         availability_status=CowAvailabilityChoices.ALIVE,
    #         current_pregnancy_status=CowPregnancyChoices.OPEN,
    #         category=CowCategoryChoices.HEIFER,
    #         current_production_status=CowProductionStatusChoices.OPEN,
    #         is_bought=True,
    #     )

    #     # Check if CowInventory is updated
    #     cow_inventory = CowInventory.objects.get(pk=1)
    #     assert cow_inventory.total_number_of_cows == 1
    #     assert cow_inventory.number_of_male_cows == 0
    #     assert cow_inventory.number_of_female_cows == 1
    #     assert cow_inventory.number_of_sold_cows == 0
    #     assert cow_inventory.number_of_dead_cows == 0

    # def test_cow_inventory_update_on_cow_update(initial_cow_inventory):
    #     # Create a new cow
    #     cow = Cow.objects.create(
    #         name="General Cow",
    #         breed=CowBreed.objects.create(name=CowBreedChoices.JERSEY),
    #         date_of_birth=todays_date - timedelta(days=370),
    #         gender=SexChoices.FEMALE,
    #         availability_status=CowAvailabilityChoices.ALIVE,
    #         current_pregnancy_status=CowPregnancyChoices.OPEN,
    #         category=CowCategoryChoices.HEIFER,
    #         current_production_status=CowProductionStatusChoices.OPEN,
    #         is_bought=True,
    #      )

    #     # Update the cow
    #     cow.name = "UpdatedCow"
    #     cow.save()

    #     # Check if CowInventory is updated
    #     cow_inventory = CowInventory.objects.get(pk=1)
    #     assert cow_inventory.total_number_of_cows == 1
    #     assert cow_inventory.number_of_male_cows == 1
    #     assert cow_inventory.number_of_female_cows == 0
    #     assert cow_inventory.number_of_sold_cows == 0
    #     assert cow_inventory.number_of_dead_cows == 0

    # def test_cow_inventory_update_on_cow_sold(sinitial_cow_inventory):
    #     # Create a new cow
    #     cow = Cow.objects.create(
    #         name="General Cow",
    #         breed=CowBreed.objects.create(name=CowBreedChoices.JERSEY),
    #         date_of_birth=todays_date - timedelta(days=370),
    #         gender=SexChoices.FEMALE,
    #         availability_status=CowAvailabilityChoices.ALIVE,
    #         current_pregnancy_status=CowPregnancyChoices.OPEN,
    #         category=CowCategoryChoices.HEIFER,
    #         current_production_status=CowProductionStatusChoices.OPEN,
    #         is_bought=True,
    #     )

    #     # Sell the cow
    #     cow.availability_status = CowAvailabilityChoices.SOLD
    #     cow.save()

    #     # Check if CowInventory is updated
    #     cow_inventory = CowInventory.objects.get(pk=1)
    #     assert cow_inventory.total_number_of_cows == 0
    #     assert cow_inventory.number_of_male_cows == 0
    #     assert cow_inventory.number_of_female_cows == 0
    #     assert cow_inventory.number_of_sold_cows == 1
    #     assert cow_inventory.number_of_dead_cows == 0

    # def test_cow_inventory_update_on_cow_dead(self, initial_cow_inventory):
    #     # Create a new cow
    #     cow = Cow.objects.create(
    #         name="General Cow",
    #         breed=CowBreed.objects.create(name=CowBreedChoices.JERSEY),
    #         date_of_birth=todays_date - timedelta(days=370),
    #         gender=SexChoices.FEMALE,
    #         availability_status=CowAvailabilityChoices.ALIVE,
    #         current_pregnancy_status=CowPregnancyChoices.OPEN,
    #         category=CowCategoryChoices.HEIFER,
    #         current_production_status=CowProductionStatusChoices.OPEN,
    #         is_bought=True,
    #     )

    #     # Mark the cow as dead
    #     cow.availability_status = CowAvailabilityChoices.DEAD
    #     cow.save()

    #     # Check if CowInventory is updated
    #     cow_inventory, created = CowInventory.objects.get_or_create(pk=1)
    #     assert cow_inventory.total_number_of_cows == 0
    #     assert cow_inventory.number_of_male_cows == 0
    #     assert cow_inventory.number_of_female_cows == 0
    #     assert cow_inventory.number_of_sold_cows == 0
    #     assert cow_inventory.number_of_dead_cows == 1

    # def test_cow_inventory_update_on_cow_delete(initial_cow_inventory):
    #     # Create a new cow
    #     cow = Cow.objects.create(
    #         name="General Cow",
    #         breed=CowBreed.objects.create(name=CowBreedChoices.JERSEY),
    #         date_of_birth=todays_date - timedelta(days=370),
    #         gender=SexChoices.FEMALE,
    #         availability_status=CowAvailabilityChoices.ALIVE,
    #         current_pregnancy_status=CowPregnancyChoices.OPEN,
    #         category=CowCategoryChoices.HEIFER,
    #         current_production_status=CowProductionStatusChoices.OPEN,
    #         is_bought=True,
    # )
    #     # Delete the cow
    #     cow.delete()

    #     # Check if CowInventory is updated
    #     cow_inventory = CowInventory.objects.get(pk=1)
    #     assert cow_inventory.total_number_of_cows == 0
    #     assert cow_inventory.number_of_male_cows == 0
    #     assert cow_inventory.number_of_female_cows == 0
    #     assert cow_inventory.number_of_sold_cows == 0
    #     assert cow_inventory.number_of_dead_cows == 0
