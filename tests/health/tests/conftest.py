from datetime import timedelta
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.choices import (
    CowAvailabilityChoices,
    CowBreedChoices,
    CowCategoryChoices,
    CowPregnancyChoices,
    CowProductionStatusChoices,
)
from core.serializers import CowSerializer
from health.choices import (
    CullingReasonChoices,
    SymptomLocationChoices,
    SymptomSeverityChoices,
    SymptomTypeChoices,
    PathogenChoices,
    DiseaseCategoryChoices,
)
from health.models import Pathogen, DiseaseCategory, Symptoms

from users.choices import SexChoices
from core.utils import todays_date


@pytest.fixture()
@pytest.mark.django_db
def setup_users():
    client = APIClient()

    # Create farm owner user
    farm_owner_data = {
        "username": "owner@example.com",
        "email": "abc1@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Owner",
        "phone_number": "+254787654321",
        "sex": SexChoices.MALE,
        "is_farm_owner": True,
    }
    farm_owner_login_data = {
        "username": "owner@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_owner_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_owner_login_data)
    farm_owner_token = response.data["auth_token"]

    # Create farm manager user
    farm_manager_data = {
        "username": "manager@example.com",
        "email": "abc2@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Manager",
        "phone_number": "+254755555555",
        "sex": SexChoices.MALE,
        "is_farm_manager": True,
    }
    farm_manager_login_data = {
        "username": "manager@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_manager_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_manager_login_data)
    farm_manager_token = response.data["auth_token"]

    # Create assistant farm manager user
    asst_farm_manager_data = {
        "username": "assistant@example.com",
        "email": "abc3@gmail.com",
        "password": "testpassword",
        "first_name": "Assistant",
        "last_name": "Farm Manager",
        "phone_number": "+254744444444",
        "sex": SexChoices.FEMALE,
        "is_assistant_farm_manager": True,
    }
    asst_farm_manager_login_data = {
        "username": "assistant@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", asst_farm_manager_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), asst_farm_manager_login_data)
    asst_farm_manager_token = response.data["auth_token"]

    # Create team leader user
    team_leader_data = {
        "username": "leader@example.com",
        "email": "abc4@gmail.com",
        "password": "testpassword",
        "first_name": "Team",
        "last_name": "Leader",
        "phone_number": "+254733333333",
        "sex": SexChoices.MALE,
        "is_team_leader": True,
    }
    team_leader_login_data = {
        "username": "leader@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", team_leader_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), team_leader_login_data)
    assert response.status_code == status.HTTP_200_OK
    team_leader_token = response.data["auth_token"]

    # Create farm worker user
    farm_worker_data = {
        "username": "worker@example.com",
        "email": "abc5@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Worker",
        "phone_number": "+254722222222",
        "sex": SexChoices.FEMALE,
        "is_farm_worker": True,
    }
    farm_worker_login_data = {
        "username": "worker@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_worker_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_worker_login_data)
    farm_worker_token = response.data["auth_token"]

    return {
        "client": client,
        "farm_owner_token": farm_owner_token,
        "farm_manager_token": farm_manager_token,
        "asst_farm_manager_token": asst_farm_manager_token,
        "team_leader_token": team_leader_token,
        "farm_worker_token": farm_worker_token,
    }


@pytest.fixture
@pytest.mark.django_db
def setup_weight_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    weight_data = {"cow": cow.id, "weight_in_kgs": 1150}
    return weight_data


@pytest.fixture
@pytest.mark.django_db
def setup_culling_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=370),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.PREGNANT,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    culling_data = {
        "cow": cow.id,
        "reason": CullingReasonChoices.COST_OF_CARE,
    }
    return culling_data


@pytest.fixture
@pytest.mark.django_db
def setup_quarantine_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.PREGNANT,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
    }

    serializer = CowSerializer(data=general_cow)
    if not serializer.is_valid():
        print(serializer.errors)
    assert serializer.is_valid()
    cow = serializer.save()

    quarantine_data = {
        "cow": cow.id,
        "reason": "Calving",
        "start_date": todays_date - timedelta(days=30),
        "end_date": todays_date,
        "notes": "Some notes",
    }

    return quarantine_data


@pytest.fixture
def setup_symptom_data():
    symptom_data = {
        "name": "Fever",
        "symptom_type": SymptomTypeChoices.RESPIRATORY,
        "date_observed": todays_date,
        "severity": SymptomSeverityChoices.MILD,
        "location": SymptomLocationChoices.WHOLE_BODY,
    }
    return symptom_data


@pytest.fixture
def setup_disease_data():
    pathogen = Pathogen.objects.create(name=PathogenChoices.UNKNOWN)
    disease_category = DiseaseCategory.objects.create(
        name=DiseaseCategoryChoices.NUTRITION
    )
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.PREGNANT,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
    }

    serializer1 = CowSerializer(data=general_cow)
    serializer2 = CowSerializer(data=general_cow)
    assert serializer1.is_valid()
    assert serializer2.is_valid()
    cow1 = serializer1.save()
    cow2 = serializer2.save()

    symptom_data = {
        "name": "Fever",
        "symptom_type": SymptomTypeChoices.RESPIRATORY,
        "date_observed": todays_date,
        "severity": SymptomSeverityChoices.MILD,
        "location": SymptomLocationChoices.WHOLE_BODY,
    }

    symptom = Symptoms.objects.create(**symptom_data)

    disease_data = {
        "name": "Brucellosis",
        "pathogen": pathogen.id,
        "category": disease_category.id,
        "occurrence_date": todays_date,
        "cows": [cow1.id, cow2.id],
        "symptoms": [symptom.id],
    }
    return disease_data
