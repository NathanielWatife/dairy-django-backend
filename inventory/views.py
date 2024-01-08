from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from inventory.filters import CowInventoryUpdateHistoryFilterSet
from inventory.models import CowInventory, CowInventoryUpdateHistory
from inventory.serializers import (
    CowInventorySerializer,
    CowInventoryUpdateHistorySerializer,
)
from users.permissions import IsFarmManager, IsFarmOwner


class CowInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to handle operations related to cow inventory.

    Provides read-only functionality for cow inventory.

    Actions:
    - list: Get the cow inventory.
           Returns a 200 response with the cow inventory data.

    Serializer class used for response data: CowInventorySerializer.

    Permissions:
    - Accessible to all authenticated users (farm workers, assistant farm managers, farm managers, farm owners).

    """

    queryset = CowInventory.objects.all()
    serializer_class = CowInventorySerializer
    permission_classes = [IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        Get the cow inventory.

        Returns a 200 response with the cow inventory data.

        """
        cow_inventory = self.get_queryset().first()

        if not cow_inventory:
            # If there is no cow inventory in the database
            return Response(
                {"detail": "No cow inventory found in the farm yet."},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(cow_inventory)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CowInventoryUpdateHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to handle operations related to cow inventory update history.

    Provides read-only functionality for cow inventory update history.

    Actions:
    - list: Get the cow inventory update history.
           Returns a 200 response with the cow inventory update history data.

    Serializer class used for response data: CowInventoryUpdateHistorySerializer.

    Permissions:
    - Accessible to all authenticated users (farm workers, assistant farm managers, farm managers, farm owners).

    """

    queryset = CowInventoryUpdateHistory.objects.all()
    serializer_class = CowInventoryUpdateHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowInventoryUpdateHistoryFilterSet
    ordering_fields = ["-date_updated"]
    permission_classes = [IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        Get the cow inventory update history.

        Returns a 200 response with the cow inventory update history data.

        """
        cow_inventory_update_history = self.get_queryset().all()

        if not cow_inventory_update_history:
            # If there is no cow inventory update history in the database
            return Response(
                {"detail": "No cow inventory update history found in the farm yet."},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(cow_inventory_update_history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
