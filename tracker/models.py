from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class FoodItem(models.Model):
    """
    Model for storing food items with their calorie count.
    This is the core model for the calorie tracking functionality.
    """
    name = models.CharField(max_length=200, help_text="Name of the food item")
    calories = models.PositiveIntegerField(help_text="Calories per serving")
    serving_size = models.CharField(max_length=100, default="1 serving", help_text="Description of serving size")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"
    
    def __str__(self):
        return f"{self.name} ({self.calories} calories)"
    
    def get_calories_display(self):
        """Return formatted calories display"""
        return f"{self.calories} calories per {self.serving_size}"

class DailyCalorieLog(models.Model):
    """
    Model for tracking daily calorie consumption.
    Stores the total calories consumed for each day.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(default=date.today, unique=True)
    total_calories = models.PositiveIntegerField(default=0, help_text="Total calories consumed today")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Calorie Log"
        verbose_name_plural = "Daily Calorie Logs"
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_calories} calories"
    
    def add_calories(self, calories):
        """Add calories to today's total"""
        self.total_calories += calories
        self.save()
    
    def reset_calories(self):
        """Reset today's calorie count to zero"""
        self.total_calories = 0
        self.save()
    
    def get_calories_remaining(self, daily_goal=2000):
        """Calculate remaining calories for the day"""
        return max(0, daily_goal - self.total_calories)

class CalorieEntry(models.Model):
    """
    Model for individual calorie entries throughout the day.
    Links food items to daily logs for detailed tracking.
    """
    daily_log = models.ForeignKey(DailyCalorieLog, on_delete=models.CASCADE, related_name='entries')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, help_text="Number of servings")
    calories_consumed = models.PositiveIntegerField(help_text="Total calories for this entry")
    consumed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Optional notes about this entry")
    
    class Meta:
        ordering = ['-consumed_at']
        verbose_name = "Calorie Entry"
        verbose_name_plural = "Calorie Entries"
    
    def __str__(self):
        return f"{self.food_item.name} - {self.calories_consumed} calories"
    
    def save(self, *args, **kwargs):
        """Override save to automatically calculate calories and update daily total"""
        if not self.calories_consumed:
            self.calories_consumed = self.food_item.calories * self.quantity
        
        # Save the entry
        super().save(*args, **kwargs)
        
        # Update the daily log total
        self.update_daily_total()
    
    def update_daily_total(self):
        """Update the daily log total calories"""
        daily_total = sum(entry.calories_consumed for entry in self.daily_log.entries.all())
        self.daily_log.total_calories = daily_total
        self.daily_log.save()
    
    def delete(self, *args, **kwargs):
        """Override delete to update daily total when entry is removed"""
        daily_log = self.daily_log
        super().delete(*args, **kwargs)
        
        # Recalculate daily total after deletion
        daily_total = sum(entry.calories_consumed for entry in daily_log.entries.all())
        daily_log.total_calories = daily_total
        daily_log.save()
