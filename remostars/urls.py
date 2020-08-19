from django.conf.urls import url
from . import views


urlpatterns = [

	url(r'^$',
		views.home,
		name='home'),

	url(r'^news/$',
		views.news,
		name='news'),

	url(r'^news/(?P<news_slug>[\w\-]+)/$',
		views.news_detail,
		name='news_detail'),

	url(r'^category/(?P<category_slug>[\w\-]+)/$',
		views.category,
		name='category'),

	url(r'^fixtures/$',
		views.fixtures,
		name='fixtures'),

	url(r'^results/$',
		views.results,
		name='results'),

	url(r'^leaguetable/$',
		views.table,
		name='table'),

	url(r'^statistics/$',
		views.statistics,
		name='statistics'),

	url(r'^players/$',
		views.players,
		name='players'),

	url(r'^players/(?P<player_slug>[\w\-]+)/$',
		views.player_detail,
		name='player_detail'),

	url(r'^officials/$',
		views.officials,
		name='officials'),

	url(r'^gallery/$',
		views.gallery,
		name='gallery'),

	url(r'^videos/$',
		views.videos,
		name='videos'),

	url(r'^contact/$',
		views.contact,
		name='contact'),

	url(r'^history/$',
		views.history,
		name='history'),

]