from django import template

register = template.Library()

@register.filter(name='makeSchedule')
def makeSchedule(company, dict):
    return company.makeSchedule(dict)