from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from health.filters import (
    WeightRecordFilterSet,
    CullingRecordFilterSet,
    QuarantineRecordFilterSet,
    DiseaseFilterSet,
    RecoveryFilterSet,
)
from health.models import (
    DiseaseCategory,
    Symptoms,
    WeightRecord,
    CullingRecord,
    QuarantineRecord,
    Pathogen,
    Disease,
    Recovery,
)
from health.serializers import (
    DiseaseCategorySerializer,
    SymptomsSerializer,
    WeightRecordSerializer,
    CullingRecordSerializer,
    QuarantineRecordSerializer,
    PathogenSerializer,
    DiseaseSerializer,
    RecoverySerializer,
)
from users.permissions import IsFarmManager, IsFarmOwner, IsAssistantFarmManager


class WeightRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to weight records.

    Provides CRUD functionality for weight records.

    Actions:
    - list: Get a list of weight records based on applied filters.
           Returns a 404 response if no weight records match the provided filters,
           and a 200 response with an empty list if there are no weight records in the database.
    - retrieve: Retrieve details of a specific weight record.
    - create: Create a new weight record.
    - update: Update an existing weight record.
    - partial_update: Partially update an existing weight record.
    - destroy: Delete an existing weight record.

    Serializer class used for request/response data: WeightRecordSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to assistant farm managers, farm managers, and farm owners only.
    - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
    - For 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = WeightRecord.objects.all()
    serializer_class = WeightRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WeightRecordFilterSet
    ordering_fields = ["-date_taken"]
    permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        List weight records based on applied filters.

        Returns a 404 response if no weight records match the provided filters,
        and a 200 response with an empty list if there are no weight records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Weight records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Weight records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CullingRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to culling records.

    Provides CRUD functionality for culling records.

    Actions:
    - list: Get a list of culling records based on applied filters.
           Returns a 404 response if no culling records match the provided filters,
           and a 200 response with an empty list if there are no culling records in the database.
    - retrieve: Retrieve details of a specific culling record.
    - create: Create a new culling record.
    - partial_update: Not allowed.
    - update: Not allowed.
    - destroy: Delete an existing culling record.

    Serializer class used for request/response data: CullingRecordSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to farm managers and farm owners only.
    - For 'create': Accessible to farm managers and farm owners only.
    - For 'partial_update', 'update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = CullingRecord.objects.all()
    serializer_class = CullingRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CullingRecordFilterSet
    ordering_fields = ["-date_carried"]
    permission_classes = [IsFarmManager | IsFarmOwner]

    def partial_update(self, request, *args, **kwargs):
        """
        Not allowed.

        Raises:
        - MethodNotAllowed: When attempting a partial update.

        """
        raise MethodNotAllowed("PATCH")

    def update(self, request, *args, **kwargs):
        """
        Not allowed.

        Raises:
        - MethodNotAllowed: When attempting a full update.

        """
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        """
        List culling records based on applied filters.

        Returns a 404 response if no culling records match the provided filters,
        and a 200 response with an empty list if there are no culling records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Culling records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Culling records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuarantineRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to quarantine records.

    Provides CRUD functionality for quarantine records.

    Actions:
    - list: Get a list of quarantine records based on applied filters.
           Returns a 404 response if no quarantine records match the provided filters,
           and a 200 response with an empty list if there are no quarantine records in the database.
    - retrieve: Retrieve details of a specific quarantine record.
    - create: Create a new quarantine record.
    - update: Update an existing quarantine record.
    - partial_update: Partially update an existing quarantine record.
    - destroy: Delete an existing quarantine record.

    Serializer class used for request/response data: QuarantineRecordSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to assistant farm managers, farm managers, and farm owners only.
    - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
    - For 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = QuarantineRecord.objects.all()
    serializer_class = QuarantineRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = QuarantineRecordFilterSet
    ordering_fields = ["-start_date"]
    permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        List quarantine records based on applied filters.

        Returns a 404 response if no quarantine records match the provided filters,
        and a 200 response with an empty list if there are no quarantine records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Quarantine records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Quarantine records found."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PathogenViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to pathogens.

    Provides CRUD functionality for pathogens.

    Actions:
    - `list`: Get a list of all pathogens.
    - `retrieve`: Retrieve details of a specific pathogen.
    - `create`: Create a new pathogen.
    - `destroy`: Delete an existing pathogen.

    Serializer class used for request/response data: `PathogenSerializer`.

    Permissions:
    - For 'list', 'retrieve', 'create', 'destroy':
      Accessible to farm managers and farm owners only.

    Attributes:
    - `queryset`: Queryset containing all `Pathogen` instances.
    - `serializer_class`: Serializer class for `Pathogen`.
    - `permission_classes`: Permission classes for controlling access to different actions.
    """

    queryset = Pathogen.objects.all()
    serializer_class = PathogenSerializer
    permission_classes = [IsFarmManager | IsFarmOwner]


class DiseaseCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to disease categories.

    Provides CRUD functionality for disease categories.

    Actions:
    - `list`: Get a list of all disease categories.
    - `retrieve`: Retrieve details of a specific disease category.
    - `create`: Create a new disease category.
    - `destroy`: Delete an existing disease category.

    Serializer class used for request/response data: `DiseaseCategorySerializer`.

    Permissions:
    - For 'list', 'retrieve', 'create', 'destroy':
      Accessible to farm managers and farm owners only.

    Attributes:
    - `queryset`: Queryset containing all `DiseaseCategory` instances.
    - `serializer_class`: Serializer class for `DiseaseCategory`.
    - `permission_classes`: Permission classes for controlling access to different actions.
    """

    queryset = DiseaseCategory.objects.all()
    serializer_class = DiseaseCategorySerializer
    permission_classes = [IsFarmManager | IsFarmOwner]


class SymptomsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to symptoms.

    Provides CRUD functionality for symptoms.

    Actions:
    - `list`: Get a list of all symptoms.
    - `retrieve`: Retrieve details of a specific symptom.
    - `create`: Create a new symptom.
    - `destroy`: Delete an existing symptom.

    Serializer class used for request/response data: `SymptomSerializer`.

    Permissions:
    - For 'list', 'retrieve', 'create', 'destroy':
      Accessible to farm managers and farm owners only.

    Attributes:
    - `queryset`: Queryset containing all `Symptom` instances.
    - `serializer_class`: Serializer class for `Symptom`.
    - `permission_classes`: Permission classes for controlling access to different actions.
    """

    queryset = Symptoms.objects.all()
    serializer_class = SymptomsSerializer
    permission_classes = [IsFarmManager | IsFarmOwner]


class DiseaseViewSet(viewsets.ModelViewSet):
    """
        ViewSet to handle operations related to diseases.
    
        Provides CRUD functionality for diseases and supports filtering and ordering.
    
        Actions:
        - `list`: Get a list of all diseases with optional filtering and ordering.
        - `retrieve`: Retrieve details of a specific disease.
        - `create`: Create a new disease.
        - `update`: Update an existing disease.
        - `partial_update`: Partially update an existing disease.
        - `destroy`: Delete an existing disease.
    
        Serializer class used for request/response data: `DiseaseSerializer`.
        Filter class used for queryset filtering: `DiseaseFilterSet`.
    
        Permissions:
        - For 'list', 'retrieve', 'create', 'update', 'partial_update', 'destroy':
          Accessible to farm managers and farm owners only.
        """
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DiseaseFilterSet
    permission_classes = [IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Disease records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Disease records found."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RecoveryViewSet(viewsets.ReadOnlyModelViewSet):
    """
       ViewSet to handle read-only operations related to recovery records.
    
       Provides read-only functionality for recovery records and supports filtering and ordering.
    
       Actions:
       - `list`: Get a list of all recovery records with optional filtering and ordering.
       - `retrieve`: Retrieve details of a specific recovery record.
    
       Serializer class used for request/response data: `RecoverySerializer`.
       Filter class used for queryset filtering: `RecoveryFilterSet`.
    
       Permissions:
       - For 'list', 'retrieve':
         Accessible to farm managers and farm owners only.
       """
    queryset = Recovery.objects.all()
    serializer_class = RecoverySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RecoveryFilterSet
    permission_classes = [IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Disease Recovery records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Disease Recovery records found."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
