from django import template

register = template.Library()

from ..models import Post, Player, Category, Result, Fixture


@register.assignment_tag
def get_latest_news():    
    return Post.objects.all()[:3]


@register.assignment_tag
def get_players():
	return Player.objects.filter(
		active=True).order_by('-id')[:4]

@register.assignment_tag
def get_categories():
	return Category.objects.all()

@register.assignment_tag
def get_latest_results():
	return Result.objects.all()[:2]
	# try:
	# 	last_match = Result.objects.latest()
	# except Result.DoesNotExist:
	# 	pass
	# return Result.objects.latest()

@register.assignment_tag
def get_upcoming_fixtures():
	return Fixture.objects.all()[:2]

