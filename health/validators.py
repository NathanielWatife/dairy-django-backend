from django.core.exceptions import ValidationError

from core.choices import CowAvailabilityChoices, CowPregnancyChoices
from core.utils import todays_date
from health.choices import (
    QuarantineReasonChoices,
    PathogenChoices,
    DiseaseCategoryChoices,
    SymptomLocationChoices,
    SymptomSeverityChoices,
    SymptomTypeChoices,
)
from users.choices import SexChoices


class WeightRecordValidator:
    """
    Provides validation methods for weight records associated with cows.

    Methods:
    - `validate_weight(weight_in_kgs)`: Validates the weight of a cow in kilograms.
    - `validate_cow_availability_status(cow)`: Validates the availability status of a cow for recording weight.
    - `validate_frequency_of_weight_records(date_taken, cow)`: Validates the frequency of weight records for a cow.

    """

    @staticmethod
    def validate_weight(weight_in_kgs):
        """
        Validates the weight of a cow in kilograms.

        Args:
        - `weight_in_kgs` (float): The weight of a cow in kilograms.

        Raises:
        - `ValidationError` with codes:
            - "invalid_weight": If the weight is less than 10 kgs or exceeds the maximum allowed weight of 1500 kgs.
        """
        if weight_in_kgs < 10:
            raise ValidationError(
                "A cow cannot weigh less than 10 kgs!", code="invalid_weight"
            )
        if weight_in_kgs > 1500:
            raise ValidationError(
                "A cow's weight cannot exceed 1500 kgs!", code="invalid_weight"
            )

    @staticmethod
    def validate_cow_availability_status(cow):
        """
        Validates the availability status of a cow for recording weight.

        Args:
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "invalid_availability_status": If the cow is not marked as alive.
        """
        if cow.availability_status != CowAvailabilityChoices.ALIVE:
            raise ValidationError(
                f"Weight records are only allowed for cows present in the farm. "
                f"This cow is marked as: {cow.availability_status}",
                code="invalid_availability_status",
            )

    @staticmethod
    def validate_frequency_of_weight_records(date_taken, cow):
        """
        Validates the frequency of weight records for a cow.

        Args:
        - `date_taken` (Date): The date when the weight record was taken.
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "duplicate_weight_record": If there is more than one weight record for
        the same cow on the same date.
        """
        from health.models import WeightRecord

        if WeightRecord.objects.filter(cow=cow, date_taken=date_taken).count() > 1:
            raise ValidationError(
                "This cow already has a weight record on this date!",
                code="duplicate_weight_record",
            )


class QuarantineValidator:
    """
    Validator class for validating quarantine-related logic.

    Methods:
    - `validate_reason`: Validate the reason for cow quarantine.
    - `validate_date`: Validate the date range for start and end dates.

    Usage:
        Use this class to perform validation checks related to cow quarantine.

    Example:
    """

    @staticmethod
    def validate_reason(reason, cow):
        """
        Validate the reason for cow quarantine.

        Parameters:
        - `reason` (str): The reason for cow quarantine.
        - `cow` (Cow): The cow to be quarantined.

        Raises:
        - `ValidationError`: If the validation fails.
            - Code: `invalid_quarantine_reason`
            - Message: "Invalid reason for cow quarantine."

        Returns:
        - None
        """
        if reason == QuarantineReasonChoices.CALVING:
            if cow.gender != SexChoices.FEMALE:
                raise ValidationError(
                    "Invalid reason for cow quarantine: Only female cows can be quarantined for 'Calving'.",
                    code="invalid_quarantine_reason",
                )

            if cow.current_pregnancy_status != CowPregnancyChoices.PREGNANT:
                raise ValidationError(
                    "Invalid reason for cow quarantine: Only pregnant female cows can be quarantined for 'Calving'.",
                    code="invalid_quarantine_reason",
                )

    @staticmethod
    def validate_date(start_date, end_date):
        """
        Validate the date range for start and end dates.

        Args:
        - `start_date` (date): The start date of the quarantine.
        - `end_date` (date or None): The end date of the quarantine.

        Raises:
        - `ValidationError`: If the date range is invalid.
            - Code: `invalid_date_range`
            - Message: "End date must be equal to or after the start date."
        """
        if start_date and end_date and start_date > end_date:
            raise ValidationError(
                "Invalid date range for quarantine: End date must be equal to or after the start date.",
                code="invalid_date_range",
            )


class PathogenValidator:
    """
    Validator class for validating pathogen-related logic.

    Methods:
    - `validate_name`: Validate the name of the pathogen.

    Usage:
        Use this class to perform validation checks related to pathogens.

    """

    @staticmethod
    def validate_name(name):
        """
        Validate the name of the pathogen.

        Parameters:
        - `name` (str): The name of the pathogen.

        Raises:
        - `ValidationError`: If the validation fails.
            - Code: `invalid_pathogen_name`
            - Message: "Invalid name for the pathogen."
        """
        if name not in PathogenChoices.values:
            raise ValidationError(
                f"Invalid name for the pathogen: {name}", code="invalid_pathogen_name"
            )


class DiseaseCategoryValidator:
    """
    Validator class for validating disease category-related logic.

    Methods:
    - `validate_name`: Validate the name of the disease category.
    """

    @staticmethod
    def validate_name(name):
        """
        Validate the name of the disease category.

        Parameters:
        - `name` (str): The name of the disease category.

        Raises:
        - `ValidationError` (code: `invalid_disease_category_name`):
            If the validation fails with the message "Invalid name: {name}".
        """
        if name not in DiseaseCategoryChoices.values:
            raise ValidationError(
                f"Invalid name: {name}", code="invalid_disease_category_name"
            )


class SymptomValidator:
    """
    Validator class for validating symptom-related logic.

    Methods:
    - `validate_fields`: Validate various fields of a symptom.
    - `validate_name`: Validate the name of the symptom.
    - `validate_type_and_location_compatibility`: Validate compatibility between symptom type and location.
    """

    @staticmethod
    def validate_fields(date_observed, symptom_type, severity, location):
        """
        Validate various fields of a symptom.

        Parameters:
        - `date_observed`: Date when the symptom was observed.
        - `symptom_type` (str): Type of the symptom.
        - `severity` (str): Severity of the symptom.
        - `location` (str): Location of the symptom.

        Raises:
        - `ValidationError` (code: `invalid_date_observed`, `invalid_symptom_type`,
          `invalid_symptom_severity`, `invalid_symptom_location`):
            If any validation fails.
        """
        if date_observed > todays_date:
            raise ValidationError("The date of observation cannot be in the future.", code="invalid_date_observed")

        if symptom_type not in SymptomTypeChoices.values:
            raise ValidationError(f"Invalid symptom type: ({symptom_type}).", code="invalid_symptom_type")

        if severity not in SymptomSeverityChoices.values:
            raise ValidationError(f"Invalid severity choice: ({severity}).", code="invalid_symptom_severity")

        if location not in SymptomLocationChoices.values:
            raise ValidationError(f"Invalid body location: ({location}).", code="invalid_symptom_location")

    @staticmethod
    def validate_name(name):
        """
        Validate the name of the symptom.

        Parameters:
        - `name` (str): The name of the symptom.

        Raises:
        - `ValidationError` (code: `invalid_symptom_name`):
            If the validation fails with the message "Symptoms name should only contain alphabetic characters (no numerics allowed)."
        """
        if not name.replace(" ", "").isalpha():
            raise ValidationError(
                "Symptoms name should only contain alphabetic characters (no numerics allowed).",
                code="invalid_symptom_name"
            )

    @staticmethod
    def validate_type_and_location_compatibility(symptom_type, location):
        """
        Validate compatibility between symptom type and location.

        Parameters:
        - `symptom_type` (str): Type of the symptom.
        - `location` (str): Location of the symptom.

        Raises:
        - `ValidationError` (code: `incompatible_type_and_location`):
            If the validation fails with the message "For respiratory symptoms, the location must be Chest, Neck, Head, or Whole Body."
        """
        if symptom_type == SymptomTypeChoices.RESPIRATORY and location not in [
            SymptomLocationChoices.CHEST,
            SymptomLocationChoices.NECK,
            SymptomLocationChoices.HEAD,
            SymptomLocationChoices.WHOLE_BODY,
        ]:
            raise ValidationError(
                "For respiratory symptoms, the location must be Chest, Neck, Head, or Whole Body.",
                code="incompatible_type_and_location"
            )
