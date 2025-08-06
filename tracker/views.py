from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.forms import formset_factory
from django.utils import timezone
from datetime import date, timedelta
from .models import FoodItem, DailyCalorieLog, CalorieEntry
from .forms import (
    FoodItemForm, CalorieEntryForm, 
    DateRangeForm, FoodSearchForm
)
from django.contrib.auth.models import User

# Helper to get or create a default user
DEFAULT_USERNAME = 'defaultuser'
def get_default_user():
    user, _ = User.objects.get_or_create(username=DEFAULT_USERNAME, defaults={'email': 'default@example.com'})
    return user

# Remove the register view
def register(request):
    pass

def dashboard(request):
    today = date.today()
    user = get_default_user()
    
    # Get or create daily log for today
    daily_log, created = DailyCalorieLog.objects.get_or_create(
        user=user, 
        date=today,
        defaults={'total_calories': 0}
    )
    
    # Get today's entries
    today_entries = CalorieEntry.objects.filter(daily_log=daily_log)
    
    # Get recent foods (last 10 added)
    recent_foods = FoodItem.objects.all().order_by('-created_at')[:6]
    
    context = {
        'daily_log': daily_log,
        'today_entries': today_entries,
        'recent_foods': recent_foods,
        'today': today,
    }
    return render(request, 'tracker/dashboard.html', context)

def food_list(request):
    search_form = FoodSearchForm(request.GET)
    foods = FoodItem.objects.all()
    
    if search_form.is_valid() and search_form.cleaned_data['search']:
        search_term = search_form.cleaned_data['search']
        foods = foods.filter(name__icontains=search_term)
    
    context = {
        'foods': foods,
        'search_form': search_form,
    }
    return render(request, 'tracker/food_list.html', context)

def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item created successfully!')
            return redirect('tracker:food_list')
    else:
        form = FoodItemForm()
    
    context = {
        'form': form,
        'title': 'Add Food Item'
    }
    return render(request, 'tracker/food_form.html', context)

def food_edit(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated successfully!')
            return redirect('tracker:food_list')
    else:
        form = FoodItemForm(instance=food)
    
    context = {
        'form': form,
        'food': food,
        'title': 'Edit Food Item'
    }
    return render(request, 'tracker/food_form.html', context)

def food_delete(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Food item deleted successfully!')
        return redirect('tracker:food_list')
    return render(request, 'tracker/food_confirm_delete.html', {'food': food})

def add_calorie_entry(request):
    today = date.today()
    user = get_default_user()
    daily_log, created = DailyCalorieLog.objects.get_or_create(
        user=user, 
        date=today,
        defaults={'total_calories': 0}
    )
    
    if request.method == 'POST':
        form = CalorieEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.daily_log = daily_log
            entry.save()
            messages.success(request, 'Calorie entry added successfully!')
            return redirect('tracker:dashboard')
    else:
        form = CalorieEntryForm()
    
    context = {
        'form': form,
        'title': 'Add Calorie Entry'
    }
    return render(request, 'tracker/calorie_entry_form.html', context)

def delete_entry(request, pk):
    entry = get_object_or_404(CalorieEntry, pk=pk, daily_log__user=get_default_user())
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('tracker:dashboard')
    return render(request, 'tracker/entry_confirm_delete.html', {'entry': entry})

def reset_calories(request):
    today = date.today()
    user = get_default_user()
    daily_log, created = DailyCalorieLog.objects.get_or_create(
        user=user, 
        date=today,
        defaults={'total_calories': 0}
    )
    
    if request.method == 'POST':
        # Delete all entries for today
        CalorieEntry.objects.filter(daily_log=daily_log).delete()
        daily_log.total_calories = 0
        daily_log.save()
        messages.success(request, 'Daily calories reset successfully!')
        return redirect('tracker:dashboard')
    
    return render(request, 'tracker/reset_confirm.html', {'daily_log': daily_log})

def reports(request):
    today = date.today()
    
    # Get date range from form
    date_form = DateRangeForm(request.GET)
    if date_form.is_valid():
        start_date = date_form.cleaned_data['start_date']
        end_date = date_form.cleaned_data['end_date']
    else:
        # Default to last 7 days
        end_date = today
        start_date = today - timedelta(days=6)
    
    # Get daily logs for the date range
    daily_logs = DailyCalorieLog.objects.filter(
        user=get_default_user(),
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # Calculate totals
    total_calories = sum(log.total_calories for log in daily_logs)
    avg_calories = total_calories / len(daily_logs) if daily_logs else 0
    
    context = {
        'daily_logs': daily_logs,
        'total_calories': total_calories,
        'avg_calories': round(avg_calories, 1),
        'start_date': start_date,
        'end_date': end_date,
        'date_form': date_form,
    }
    return render(request, 'tracker/reports.html', context)

def get_food_data(request):
    """AJAX endpoint to get food nutritional data"""
    food_id = request.GET.get('food_id')
    if food_id:
        try:
            food = FoodItem.objects.get(pk=food_id)
            return JsonResponse({
                'calories': food.calories_per_100g,
                'protein': float(food.protein_per_100g),
                'carbs': float(food.carbs_per_100g),
                'fat': float(food.fat_per_100g),
            })
        except FoodItem.DoesNotExist:
            return JsonResponse({'error': 'Food not found'}, status=404)
    return JsonResponse({'error': 'No food ID provided'}, status=400)
