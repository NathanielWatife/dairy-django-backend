from django.urls import path, include
from rest_framework import routers

from health.views import (
    DiseaseCategoryViewSet,
    SymptomsViewSet,
    WeightRecordViewSet,
    CullingRecordViewSet,
    QuarantineRecordViewSet,
    PathogenViewSet,
    DiseaseViewSet,
    RecoveryViewSet,
    TreatmentViewSet,
)

app_name = 'health'

router = routers.DefaultRouter()
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')
router.register(r'culling-records', CullingRecordViewSet, basename='culling-records')
router.register(r'quarantine-records', QuarantineRecordViewSet, basename='quarantine-records')
router.register(r'pathogens', PathogenViewSet, basename='pathogens')
router.register(r'disease-categories', DiseaseCategoryViewSet, basename='disease-categories')
router.register(r'symptoms', SymptomsViewSet, basename='symptoms')
router.register(r'diseases', DiseaseViewSet, basename='diseases')
router.register(r'disease-recoveries', RecoveryViewSet, basename='disease-recoveries')
router.register(r'disease-treatments', TreatmentViewSet, basename='disease-treatments')

urlpatterns = [
    path('', include(router.urls))
]
