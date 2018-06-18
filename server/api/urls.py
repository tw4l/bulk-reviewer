from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('transfer/', views.ListTransfer.as_view()),
    path('transfer/<uuid:pk>/', views.DetailTransfer.as_view()),
    path('file/<uuid:pk>/', views.DetailFile.as_view()),
    path('file/<uuid:pk>/features/', views.ListFeature.as_view()),
    path('feature/<uuid:pk>/', views.DetailFeature.as_view()),
    path('config/', views.ListBEConfig.as_view()),
    path('config/<uuid:pk>/', views.DetailBEConfig.as_view()),
    path('session/', views.ListBESession.as_view()),
    path('session/<uuid:pk>/', views.DetailBESession.as_view()),
    path('session/<uuid:pk>/files/', views.ListFile.as_view()),
    path('session/<uuid:pk>/features/', views.ListFeatureBySession.as_view()),
    path('session/<uuid:pk>/bulk_extractor/', views.bulk_extractor, name='bulk_extractor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
