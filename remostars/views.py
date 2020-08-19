from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import Post, Fixture, Result, Player, ClubOfficial, About, ClubHonor, Photo, YoutubeVideo, Category, Statistic, Sponsor, ClubIndex
from datetime import datetime


PAGINATION = 20

def mk_paginator(request, items, num_items):
    '''Create and return a paginator.'''
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get('page', '1'))
    except ValueError: page = 1
    try: items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def home(request):
	try:
		last_match = Result.objects.latest()
	except Result.DoesNotExist:
		pass
	try:
		next_match = Fixture.objects.earliest()
	except Fixture.DoesNotExist:
		pass
	sponsors = Sponsor.objects.all()
	return render(request,
		'remostars/home.html',
		locals())

def news(request):
	news_list = Post.objects.all()
	news_list = mk_paginator(request, news_list, PAGINATION)

	return render(request,
		'remostars/news.html',
		locals())

def news_detail(request, news_slug):
	news = get_object_or_404(Post,
		slug__iexact=news_slug)

	return render(request,
		'remostars/news_detail.html',
		locals())

def category(request, category_slug):
	category = get_object_or_404(Category,
		slug__iexact=category_slug)
	news_list = Post.objects.filter(
	    category=category)
	news_list = mk_paginator(request, news_list, PAGINATION)

	return render(request,
		'remostars/category.html',
		locals())

def fixtures(request):
	fixtures = Fixture.objects.all()
	fixtures = mk_paginator(request, fixtures, PAGINATION)

	return render(request,
		'remostars/fixtures.html',
		locals())

def results(request):
	results = Result.objects.all()
	results = mk_paginator(request, results, PAGINATION)

	return render(request,
		'remostars/results.html',
		locals())

def statistics(request):
	statistics = Statistic.objects.filter(
		player__active=True).filter(
		active=True)

	return render(request,
		'remostars/statistics.html',
		locals())

def players(request):
	goalkeepers = Player.objects.filter(
		position__iexact='Goalkeeper',
		active=True)
	defenders = Player.objects.filter(
		position__iexact='Defender',
		active=True)
	midfielders = Player.objects.filter(
		position__iexact='Midfielder',
		active=True)
	strikers = Player.objects.filter(
		position__iexact='Striker',
		active=True)

	return render(request,
		'remostars/players.html',
		locals())

def player_detail(request, player_slug):
	player = get_object_or_404(Player,
		slug__iexact=player_slug)

	return render(request,
		'remostars/player_detail.html',
		locals())

def officials(request):
	officials = ClubOfficial.objects.filter(
		active=True)

	return render(request,
		'remostars/officials.html',
		locals())

def gallery(request):
	photos = Photo.objects.all()
	photos = mk_paginator(request, photos, PAGINATION)

	return render(request,
		'remostars/gallery.html',
		locals())

def contact(request):

	return render(request,
		'remostars/contact.html',
		locals())

def history(request):
	try:
		about = About.objects.get()
	except About.DoesNotExist:
		pass
	honors = ClubHonor.objects.all()

	return render(request,
		'remostars/history.html',
		locals())

def videos(request):
	videos = YoutubeVideo.objects.all()

	return render(request,
		'remostars/videos.html',
		locals())

def table(request):
    league_table = ClubIndex.objects.all()
    return render(
        request,
        'remostars/table.html',
        locals())
