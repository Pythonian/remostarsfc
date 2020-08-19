from django.contrib import admin
from .models import Category, Post, Club, Fixture, Result, Player, ClubOfficial, About, ClubHonor, Photo, YoutubeVideo, Statistic, Sponsor


def default_rank(modeladmin, request, queryset):
    '''This formats the club rank datas to default zero.'''
    queryset.update(played=0, wins=0, draws=0, loss=0, goals_for=0, goals_against=0, goals_difference=0, points=0)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	list_display = ['name', 'position', 'squad_number', 'goals', 'club_appearances', 'yellow_cards', 'red_cards', 'active']
	list_filter = ['position']
	list_editable = ['goals', 'club_appearances', 'yellow_cards', 'red_cards']


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'match_date', 'venue']


@admin.register(ClubOfficial)
class ClubOfficialAdmin(admin.ModelAdmin):
	list_display = ['name', 'position']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'match_date']


@admin.register(ClubHonor)
class ClubHonorAdmin(admin.ModelAdmin):
	list_display = ['achievement', 'year']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'goals', 'appearances', 'yellow_cards', 'red_cards']
	list_editable = ['goals', 'appearances', 'yellow_cards', 'red_cards']



admin.site.register(Club)
admin.site.register(About)
admin.site.register(Photo)
admin.site.register(YoutubeVideo)
admin.site.register(Sponsor)
