from django import template
import calendar

register = template.Library()

@register.filter(name="by_hallazgo")
def by_hallazgo(pics, source_id):
    return pics.filter(hallazgo__source_id= source_id)

@register.filter(name="avg")
def avg(value, total):
    return "❚" * int(100 * value/total)

@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]
