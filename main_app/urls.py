from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),

    path('cars/<int:car_id>/add_gas/', views.add_gas, name='add_gas'),

    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),

    path('cars/<int:car_id>/assoc_feature/<int:feature_id>/', views.assoc_feature, name='assoc_feature'),
    path('cats/<int:cat_id>/unassoc_feature/<int:feature_id>/', views.unassoc_feature, name='unassoc_feature'),

    path('features/', views.Featurelist.as_view(), name='features_index'),
    path('features/<int:pk>/', views.FeatureDetail.as_view(), name='features_detail'),
    path('features/create/', views.FeatureCreate.as_view(), name='features_create'),
    path('features/<int:pk>/update/', views.FeatureUpdate.as_view(), name='features_update'),
    path('features/<int:pk>/delete/', views.FeatureDelete.as_view(), name='features_delete'),

     path('accounts/', include('django.contrib.auth.urls')),
     path('accounts/signup', views.signup, name='signup'),
]
