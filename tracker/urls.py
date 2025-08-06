from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Authentication
    # path('register/', views.register, name='register'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Food management
    path('foods/', views.food_list, name='food_list'),
    path('foods/add/', views.add_food, name='add_food'),
    path('foods/<int:pk>/edit/', views.food_edit, name='food_edit'),
    path('foods/<int:pk>/delete/', views.food_delete, name='food_delete'),
    
    # Calorie tracking
    path('add-entry/', views.add_calorie_entry, name='add_calorie_entry'),
    path('entry/<int:pk>/delete/', views.delete_entry, name='delete_entry'),
    path('reset/', views.reset_calories, name='reset_calories'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # AJAX endpoints
    path('api/food-data/', views.get_food_data, name='get_food_data'),
] 