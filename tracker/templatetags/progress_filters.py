from django import template

register = template.Library()

@register.filter
def progress_width_class(value, goal=None):
    """
    Convert a percentage value to a CSS class name for progress bar width.
    If goal is provided, calculates the percentage as (value/goal)*100.
    Rounds to the nearest 5% increment.
    """
    try:
        if goal is not None and float(goal) > 0:
            # Calculate percentage from value and goal
            percentage = (float(value) / float(goal)) * 100
        else:
            # Use value directly as percentage
            percentage = float(value)
        
        # Round to nearest 5
        percentage = round(percentage / 5) * 5
        # Ensure it's between 0 and 100
        percentage = max(0, min(100, percentage))
        return f"progress-width-{int(percentage)}"
    except (ValueError, TypeError):
        return "progress-width-0" 