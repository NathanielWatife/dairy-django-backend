from django_filters import rest_framework as filters

from inventory.models import CowInventoryUpdateHistory


class CowInventoryUpdateHistoryFilterSet(filters.FilterSet):
    """
    Filter set for querying Cow Inventory Update History instances based on specific criteria.

    Filters:
    - `year`: An exact match filter for the year of the update history.
    - `month`: An exact match filter for the month of the update history.

    Meta:
    - `model`: The Cow Inventory Update History model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'year' and 'month'.

    Usage:
        Use this filter set to apply filters when querying the list of Cow Inventory Update History instances.
        For example, to retrieve all update histories from a specific year and month.

    Example:
        ```
        /api/cow-inventory-update-histories/?year=2023&month=5
        ```
    """
    year = filters.NumberFilter(field_name="date_updated__year", lookup_expr="exact")
    month = filters.NumberFilter(field_name="date_updated__month", lookup_expr="exact")

    class Meta:
        model = CowInventoryUpdateHistory
        fields = ["year", "month"]

