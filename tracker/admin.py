from django.contrib import admin
from .models import FoodItem, DailyCalorieLog, CalorieEntry

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    """Admin interface for FoodItem model"""
    list_display = ['name', 'calories', 'serving_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Food Information', {
            'fields': ('name', 'calories', 'serving_size')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DailyCalorieLog)
class DailyCalorieLogAdmin(admin.ModelAdmin):
    """Admin interface for DailyCalorieLog model"""
    list_display = ['user', 'date', 'total_calories', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Log Information', {
            'fields': ('user', 'date', 'total_calories')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CalorieEntry)
class CalorieEntryAdmin(admin.ModelAdmin):
    """Admin interface for CalorieEntry model"""
    list_display = ['food_item', 'daily_log', 'quantity', 'calories_consumed', 'consumed_at']
    list_filter = ['consumed_at', 'daily_log__date']
    search_fields = ['food_item__name', 'daily_log__user__username']
    ordering = ['-consumed_at']
    readonly_fields = ['consumed_at']
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('daily_log', 'food_item', 'quantity', 'calories_consumed', 'notes')
        }),
        ('Timestamps', {
            'fields': ('consumed_at',),
            'classes': ('collapse',)
        }),
    )
