from rest_framework import serializers
from reproduction.models import Pregnancy, Heat, Insemination


class PregnancySerializer(serializers.ModelSerializer):
    """
    Serializer for the Pregnancy model.

    Fields:
    - `id`: A read-only field representing the unique identifier of the pregnancy.
    - `cow`: A nested serializer field representing the cow associated with the pregnancy.
    - `start_date`: A date field representing the start date of the pregnancy.
    - `date_of_calving`: A date field representing the date of calving.
    - `pregnancy_status`: A choice field representing the status of the pregnancy.
    - `pregnancy_notes`: A text field representing notes related to the pregnancy.
    - `calving_notes`: A text field representing notes related to calving.
    - `pregnancy_scan_date`: A date field representing the date of pregnancy scanning.
    - `pregnancy_failed_date`: A date field representing the date when the pregnancy failed.
    - `pregnancy_outcome`: A choice field representing the outcome of the pregnancy.

    Meta:
    - `model`: The Pregnancy model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Pregnancy model instances to JSON representations
        and vice versa. It includes read-only fields for additional information such as
        pregnancy duration and due date.

    Example:
        ```
        class Pregnancy(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            start_date = models.DateField()
            date_of_calving = models.DateField()
            pregnancy_status = models.CharField(max_length=50, choices=PregnancyStatusChoices.choices)
            pregnancy_notes = models.TextField()
            calving_notes = models.TextField()
            pregnancy_scan_date = models.DateField()
            pregnancy_failed_date = models.DateField()
            pregnancy_outcome = models.CharField(max_length=50, choices=PregnancyOutcomeChoices.choices)

        class PregnancySerializer(serializers.ModelSerializer):
            due_date = serializers.ReadOnlyField()
            pregnancy_duration = serializers.ReadOnlyField()

            class Meta:
                model = Pregnancy
                fields = ("id", "cow", "start_date", "date_of_calving", "pregnancy_status", "pregnancy_notes",
                          "calving_notes", "pregnancy_scan_date", "pregnancy_failed_date", "pregnancy_outcome",
                          "pregnancy_duration", "due_date")
        ```
    """

    class Meta:
        model = Pregnancy
        fields = (
            "id",
            "cow",
            "start_date",
            "date_of_calving",
            "pregnancy_status",
            "pregnancy_notes",
            "calving_notes",
            "pregnancy_scan_date",
            "pregnancy_failed_date",
            "pregnancy_outcome",
            "pregnancy_duration",
            "due_date",
        )


class HeatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Heat model.

    Fields:
    - `id`: A read-only field representing the unique identifier of the heat observation.
    - `cow`: A nested serializer field representing the cow associated with the heat observation.
    - `observation_time`: A datetime field representing the time of the heat observation.

    Meta:
    - `model`: The Heat model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Heat model instances to JSON representations and vice versa.

    Example:
        ```
        class Heat(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            observation_time = models.DateTimeField()

        class HeatSerializer(serializers.ModelSerializer):
            class Meta:
                model = Heat
                fields = ("id", "cow", "observation_time")
        ```
    """

    class Meta:
        model = Heat
        fields = ("id", "cow", "observation_time")


class InseminationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Insemination model.

    Fields:
    - `cow`: A nested serializer field representing the cow associated with the insemination.
    - `date_of_insemination`: A datetime field representing the date of the insemination.
    - `pregnancy`: A nested serializer field representing the associated pregnancy.
    - `inseminator`: A nested serializer field representing the inseminator.
    - `success`: A boolean field representing the success status of the insemination.
    - `notes`: A text field representing any additional notes for the insemination.
    - `days_since_insemination`: A read-only field representing the number of days since the insemination.

    Meta:
    - `model`: The Insemination model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Insemination model instances to JSON representations and vice versa.

    Example:
        ```
        class Insemination(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name="inseminations")
            date_of_insemination = models.DateTimeField(default=timezone.now)
            pregnancy = models.OneToOneField(Pregnancy, on_delete=models.PROTECT, editable=False, null=True)
            success = models.BooleanField(default=False)
            notes = models.TextField(null=True)
            inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT, related_name="inseminations_done")

        class InseminationSerializer(serializers.ModelSerializer):
            days_since_insemination = serializers.ReadOnlyField()

            class Meta:
                model = Insemination
                fields = (
                    "cow",
                    "date_of_insemination",
                    "pregnancy",
                    "inseminator",
                    "success",
                    "notes",
                    "days_since_insemination"
                )
        ```
    """

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "cow",
            "date_of_insemination",
            "pregnancy",
            "inseminator",
            "semen",
        ]
        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)

    class Meta:
        model = Insemination
        fields = (
            "cow",
            "date_of_insemination",
            "pregnancy",
            "inseminator",
            "success",
            "notes",
            "days_since_insemination",
        )
