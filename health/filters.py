from django_filters import rest_framework as filters

from health.models import (
    WeightRecord,
    CullingRecord,
    QuarantineRecord,
    Disease,
    Recovery,
    Treatment,
)


class WeightRecordFilterSet(filters.FilterSet):
    """
    Filter set for querying WeightRecord instances based on specific criteria.

    Filters:
    - `cow`: A filter for the cow associated with the weight record (case-insensitive contains search).
    - `day_of_weighing`: An exact match filter for the day of the weighing date.
    - `month_of_weighing`: An exact match filter for the month of the weighing date.
    - `year_of_weighing`: An exact match filter for the year of the weighing date.

    Meta:
    - `model`: The WeightRecord model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow', 'day_of_weighing', 'month_of_weighing', and 'year_of_weighing'.

    Usage:
        Use this filter set to apply filters when querying the list of WeightRecord instances.
        For example, to retrieve all weight records for a specific cow.

    Example:
        ```
        /api/weight_records/?cow=123
        ```
    """

    cow = filters.CharFilter(field_name="cow", lookup_expr="icontains")
    day_of_weighing = filters.NumberFilter(
        field_name="date_taken__day", lookup_expr="exact"
    )
    month_of_weighing = filters.NumberFilter(
        field_name="date_taken__month", lookup_expr="exact"
    )
    year_of_weighing = filters.NumberFilter(
        field_name="date_taken__year", lookup_expr="exact"
    )

    class Meta:
        model = WeightRecord
        fields = [
            "cow",
            "day_of_weighing",
            "month_of_weighing",
            "year_of_weighing",
        ]


class CullingRecordFilterSet(filters.FilterSet):
    """
    Filter set for querying CullingRecord instances based on specific criteria.

    Filters:
    - `reason`: A filter for the reason of culling (case-insensitive contains search).
    - `month_of_culling`: An exact match filter for the month of the culling date.
    - `year_of_culling`: An exact match filter for the year of the culling date.

    Meta:
    - `model`: The CullingRecord model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'reason', 'month_of_culling', and 'year_of_culling'.

    Usage:
        Use this filter set to apply filters when querying the list of CullingRecord instances.
        For example, to retrieve all culling records with a specific reason.

    Example:
        ```
        /api/culling_records/?reason=cost
        ```
    """

    reason = filters.CharFilter(field_name="reason", lookup_expr="icontains")
    month_of_culling = filters.NumberFilter(
        field_name="date_carried__month", lookup_expr="exact"
    )
    year_of_culling = filters.NumberFilter(
        field_name="date_carried__year", lookup_expr="exact"
    )

    class Meta:
        model = CullingRecord
        fields = ["reason", "year_of_culling", "month_of_culling"]


class QuarantineRecordFilterSet(filters.FilterSet):
    """
    Filter set for querying QuarantineRecord instances based on specific criteria.

    Filters:
    - `reason`: A filter for the quarantine reason (exact match).
    - `start_date`: An exact match filter for the start date.
    - `end_date`: An exact match filter for the end date.

    Meta:
    - `model`: The QuarantineRecord model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'reason', 'start_date', and 'end_date'.

    Usage:
        Use this filter set to apply filters when querying the list of QuarantineRecord instances.
        For example, to retrieve all quarantine records for a specific reason.

    Example:
        ```
        /api/quarantine_records/?reason=some_reason
        ```
    """

    reason = filters.CharFilter(field_name="reason", lookup_expr="exact")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="exact")
    end_date = filters.DateFilter(field_name="end_date", lookup_expr="exact")

    class Meta:
        model = QuarantineRecord
        fields = [
            "reason",
            "start_date",
            "end_date",
        ]


class DiseaseFilterSet(filters.FilterSet):
    """
    Filter set for querying Disease instances based on specific criteria.

    Filters:
    - `cows`: A filter for cows related to the disease (case-insensitive contains).
    - `pathogen`: A filter for the pathogen causing the disease (case-insensitive contains).
    - `category`: A filter for the disease category (case-insensitive contains).
    - `occurrence_date`: A filter for the occurrence date of the disease (case-insensitive contains).

    Meta:
    - `model`: The Disease model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cows', 'pathogen', 'category', and 'occurrence_date'.

    Usage:
        Use this filter set to apply filters when querying the list of Disease instances.
        For example, to retrieve all diseases related to a specific cow.

    Example:
        ```
        /api/diseases/?cows=some_cow
        ```
    """

    cows = filters.CharFilter(field_name="cows", lookup_expr="icontains")
    pathogen = filters.CharFilter(field_name="pathogen", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")
    occurrence_date = filters.CharFilter(
        field_name="occurrence_date", lookup_expr="icontains"
    )

    class Meta:
        model = Disease
        fields = ["cows", "pathogen", "category", "occurrence_date"]


class RecoveryFilterSet(filters.FilterSet):
    """
    Filter set for querying Recovery instances based on specific criteria.

    Filters:
    - `cow`: A filter for cows recovering from a disease (case-insensitive contains).
    - `disease`: A filter for the disease from which cows are recovering (case-insensitive contains).

    Meta:
    - `model`: The Recovery model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow' and 'disease'.

    Usage:
        Use this filter set to apply filters when querying the list of Recovery instances.
        For example, to retrieve all recovery records for a specific cow.

    Example:
        ```
        /api/disease-recoveries/?cow=some_cow
        ```
    """

    cow = filters.CharFilter(field_name="cow", lookup_expr="icontains")
    disease = filters.CharFilter(field_name="disease", lookup_expr="icontains")

    class Meta:
        model = Recovery
        fields = ["cow", "disease"]


class TreatmentFilterSet(filters.FilterSet):
    """
    Filter set for querying Treatment instances based on specific criteria.

    Filters:
    - `cow`: A filter for cows undergoing treatment (case-insensitive contains).
    - `disease`: A filter for the disease for which cows are receiving treatment (case-insensitive contains).

    Meta:
    - `model`: The Treatment model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow' and 'disease'.

    Usage:
        Use this filter set to apply filters when querying the list of Treatment instances.
        For example, to retrieve all treatment records for a specific cow.

    Example:
        ```
        /api/diseases-treatments/?cow=cow
        ```
    """

    cow = filters.CharFilter(field_name="cow", lookup_expr="icontains")
    disease = filters.CharFilter(field_name="disease", lookup_expr="icontains")

    class Meta:
        model = Treatment
        fields = ["cow", "disease"]
