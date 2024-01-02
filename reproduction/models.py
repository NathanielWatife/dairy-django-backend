from django.db import models
from django.utils import timezone

from core.models import Cow, Inseminator
from reproduction.choices import PregnancyStatusChoices, PregnancyOutcomeChoices
from reproduction.managers import PregnancyManager, InseminationManager
from reproduction.validators import (
    PregnancyValidator,
    HeatValidator,
    InseminationValidator,
)


class Pregnancy(models.Model):
    """
    Represents a pregnancy record associated with a specific cow in the dairy farm.

    Attributes:
    - `cow` (Cow): The cow associated with the pregnancy.
    - `start_date` (date): The start date of the pregnancy.
    - `date_of_calving` (date or None): The date of calving, if applicable.
    - `pregnancy_status` (str): The current status of the pregnancy.
    - `pregnancy_notes` (str or None): Additional notes related to the pregnancy.
    - `calving_notes` (str or None): Additional notes related to calving.
    - `pregnancy_scan_date` (date or None): The date of pregnancy scanning, if applicable.
    - `pregnancy_failed_date` (date or None): The date of pregnancy failure, if applicable.
    - `pregnancy_outcome` (str or None): The outcome of the pregnancy.

    Methods:
    - `pregnancy_duration`: Returns the number of days since the inception of pregnancy.
    - `due_date`: Returns the due date of the pregnancy.

    Custom Managers:
    - `objects` (PregnancyManager): Custom manager for handling pregnancy-related operations.

    Overrides:
    - `clean`: Performs validation checks before saving the pregnancy record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If pregnancy record validation fails.
    """

    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name="pregnancies")
    start_date = models.DateField()
    date_of_calving = models.DateField(null=True)
    pregnancy_status = models.CharField(
        max_length=11,
        choices=PregnancyStatusChoices.choices,
        default=PregnancyStatusChoices.UNCONFIRMED,
    )
    pregnancy_notes = models.TextField(null=True)
    calving_notes = models.TextField(null=True)
    pregnancy_scan_date = models.DateField(null=True)
    pregnancy_failed_date = models.DateField(null=True)
    pregnancy_outcome = models.CharField(
        max_length=11, choices=PregnancyOutcomeChoices.choices, null=True
    )

    objects = PregnancyManager()

    @property
    def pregnancy_duration(self):
        """
        Returns the number of days since the inception of pregnancy.
        """
        return PregnancyManager.pregnancy_duration(self)

    @property
    def due_date(self):
        """
        Returns the due date of the pregnancy.
        """
        return PregnancyManager.due_date(self)

    def clean(self):
        """
        Performs validation checks before saving the pregnancy record.

        Raises:
        - `ValidationError`: If pregnancy record validation fails.
        """
        PregnancyValidator.validate_age(self.cow.age, self.start_date, self.cow)
        PregnancyValidator.validate_cow_current_pregnancy_status(self.cow)
        PregnancyValidator.validate_cow_availability_status(self.cow)
        PregnancyValidator.validate_dates(
            self.start_date,
            self.date_of_calving,
        )
        PregnancyValidator.validate_pregnancy_status(
            self.pregnancy_status,
            self.start_date,
            self.pregnancy_failed_date,
            self.pregnancy_duration,
        )
        PregnancyValidator.validate_outcome(
            self.pregnancy_outcome, self.pregnancy_status, self.date_of_calving
        )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Heat(models.Model):
    """
    Represents a record of heat observation in a cow.

    Attributes:
    - `observation_time` (datetime): The time of heat observation.
    - `cow` (Cow): The cow associated with the heat observation.

    Methods:
    - `__str__`: Returns a string representation of the heat record.

    Overrides:
    - `clean`: Performs validation checks before saving the heat record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If heat record validation fails.
    """

    observation_time = models.DateTimeField(default=timezone.now, editable=False)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="heat_records")

    def __str__(self):
        """
        Returns a string representation of the heat record.
        """
        return f"Heat record for cow {self.cow.tag_number} on {self.observation_time}"

    def clean(self):
        """
        Performs validation checks before saving the heat record.

        Raises:
        - `ValidationError`: If heat record validation fails.
        """
        HeatValidator.validate_pregnancy(self.cow)
        HeatValidator.validate_production_status(self.cow)
        HeatValidator.validate_dead(self.cow)
        HeatValidator.validate_gender(self.cow)
        HeatValidator.validate_within_60_days_after_calving(
            self.cow, self.observation_time
        )
        HeatValidator.validate_within_21_days_of_previous_heat(
            self.cow, self.observation_time
        )
        HeatValidator.validate_min_age(self.cow)
        HeatValidator.validate_already_in_heat(self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Insemination(models.Model):
    """
    Represents a record of insemination in a cow.

    Attributes:
    - `cow` (Cow): The cow associated with the insemination record.
    - `pregnancy` (Pregnancy): The pregnancy associated with the insemination record.
    - `success` (bool): Indicates the success of the insemination.
    - `notes` (str): Additional notes related to the insemination.
    - `inseminator` (Inseminator): The inseminator responsible for the insemination.
    - `date_of_insemination` (datetime): The time of insemination.

    Methods:
    - `__str__`: Returns a string representation of the insemination record.
    - `days_since_insemination`: Returns the number of days since the insemination.

    Overrides:
    - `clean`: Performs validation checks before saving the insemination record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If insemination record validation fails.
    """

    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name="inseminations")
    pregnancy = models.OneToOneField(
        Pregnancy, on_delete=models.PROTECT, editable=False, null=True
    )
    success = models.BooleanField(default=False)
    notes = models.TextField(null=True)
    inseminator = models.ForeignKey(
        Inseminator, on_delete=models.PROTECT, related_name="inseminations_done"
    )
    date_of_insemination = models.DateTimeField(default=timezone.now)

    objects = InseminationManager()

    @property
    def days_since_insemination(self):
        """
        Returns the number of days since the insemination.
        """
        return Insemination.objects.days_since_insemination(self)

    def __str__(self):
        """
        Returns a string representation of the insemination record.
        """
        return f"Insemination record for cow {self.cow.tag_number} on {self.date_of_insemination}"

    def clean(self):
        """
        Performs validation checks before saving the insemination record.

        Raises:
        - `ValidationError`: If insemination record validation fails.
        """
        InseminationValidator.validate_within_21_days_of_previous_insemination(
            self.pk, self.cow
        )
        InseminationValidator.validate_already_in_heat(
            self.cow, self.date_of_insemination
        )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
