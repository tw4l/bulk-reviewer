from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('file/<uuid:pk>/', views.DetailFile.as_view()),
    path('file/<uuid:pk>/features/', views.ListFeature.as_view()),
    path('file/<uuid:pk>/entities/', views.ListNamedEntities.as_view()),
    path('feature/<uuid:pk>/', views.DetailFeature.as_view()),
    path('config/add/', views.CreateBEConfig.as_view()),
    path('config/<uuid:pk>/', views.DetailBEConfig.as_view()),
    path('config/', views.ListBEConfig.as_view()),
    path('session/add/', views.CreateBESession.as_view()),
    path('session/<uuid:pk>/', views.DetailBESession.as_view()),
    path('session/<uuid:pk>/files/', views.ListFile.as_view()),
    path('session/<uuid:pk>/features/', views.ListFeatureBySession.as_view()),
    path('session/<uuid:pk>/entities/', views.ListNamedEntitiesBySession.as_view()),
    path('session/<uuid:pk>/redacted_sets/', views.ListRedactedSetBySession.as_view()),
    path('session/<uuid:pk>/csv_reports/', views.download_csv_reports),
    path('session/<uuid:pk>/dfxml/', views.download_dfxml),
    path('session/<uuid:pk>/bulk_extractor_reports/', views.download_be_reports),
    path('session/', views.ListBESession.as_view()),
    path('redacted_set/add/', views.CreateRedactedSet.as_view()),
    path('redacted_set/<uuid:pk>/', views.DetailRedactedSet.as_view()),
    path('redacted_set/', views.ListRedactedSet.as_view()),
    path('batch_feature_update/', views.UpdateFeatureList.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
