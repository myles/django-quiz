from django.template import Library

register = Library()

@register.filter
def intequaltest(value, arg):
	
	return (value == arg)
