# Python libraries
from __future__ import unicode_literals
import datetime

# Django modules
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible

# Third-party Django apps
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        help_text='Maximum of 50 characters.')
    slug = models.SlugField(
        unique=True,
        help_text='URL automatically generated from the title.')

    class Meta:
        ordering = ['title']
        verbose_name_plural ="Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'category',
            args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(
    	max_length=250,
    	unique=True)
    slug = models.SlugField(
        max_length=250,
        unique=True)
    image = ProcessedImageField(
        upload_to="images",
        processors = [ResizeToFill(750, 400)],
        format = 'JPEG',
        options = {'quality': 100})
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Image Caption. Optional")
    excerpt = models.TextField(
        help_text='Summary of the Blog Post.')
    body = RichTextField()
    created = models.DateTimeField(
        auto_now_add=True)
    updated = models.DateTimeField(
    	auto_now=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True)

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'

    def get_previous_post(self):
        return self.get_previous_by_created()

    def get_next_post(self):
        return self.get_next_by_created()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'news_detail',
            kwargs={'news_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
	        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Club(models.Model):
	name = models.CharField(
		max_length=50)
	logo = models.ImageField(
		upload_to='logos')

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


def default_start_time():
    '''Default time for the Matches.'''
    now   = datetime.datetime.now()
    start = now.replace(
    	hour=16, minute=0,
    	second=0, microsecond=0)
    return start

class FixtureManager(models.Manager):
	def get_queryset(self):
		return super(FixtureManager, self).get_queryset().filter(
			match_date__gte=datetime.datetime.now())

@python_2_unicode_compatible
class Fixture(models.Model):
	match_type = models.CharField(
	    max_length=50,
	    help_text="E.g: NPFL Matchday 1")
	home_team = models.ForeignKey(
	    Club, related_name="fixture_home_team")
	away_team = models.ForeignKey(
	    Club, related_name="fixture_away_team")
	match_date = models.DateField()
	match_time = models.TimeField(
	    default=default_start_time,
	    help_text="Default is 16:00:00 for 4p.m.")
	venue = models.CharField(max_length=50, #increase to 100
		help_text='Name and Location of the Stadium, E.g. Teslim Balogun Stadium, Lagos.')
	objects = FixtureManager()

	class Meta:
		ordering = ['match_date']
		get_latest_by = 'match_date'

	def __str__(self):
	    return "%s v %s - %s" % (
	        self.home_team, self.away_team, self.match_type)


class ResultManager(models.Manager):
	def get_queryset(self):
		return super(ResultManager, self).get_queryset().filter(
			match_date__lte=datetime.datetime.now())

@python_2_unicode_compatible
class Result(models.Model):
	match_type = models.CharField(
	    max_length=50,
	    help_text="E.g: NPFL Matchday 1")
	home_team = models.ForeignKey(
	    Club, related_name="result_home_team")
	home_team_score = models.PositiveIntegerField()
	away_team = models.ForeignKey(
	    Club, related_name="result_away_team")
	away_team_score = models.PositiveIntegerField()
	match_date = models.DateField()
	match_time = models.TimeField(
	    default=default_start_time,
	    help_text="Default is 16:00:00 for 4p.m.")
	venue = models.CharField(max_length=50,
		help_text='Name and Location of the Stadium, E.g. Teslim Balogun Stadium, Lagos.')
	objects = ResultManager()

	class Meta:
		ordering = ['-match_date']
		get_latest_by = 'match_date'

	def __str__(self):
	    return "%s %d:%d %s" % (
	        self.home_team, self.home_team_score,
	        self.away_team_score, self.away_team)


@python_2_unicode_compatible
class ClubOfficial(models.Model):
	name = models.CharField(
		max_length=100)
	image = models.ImageField(
		upload_to='officials')
	position = models.CharField(
		max_length=100)
	active = models.BooleanField(
		default=True,
		help_text='Uncheck this if the Official is no longer with the club.')

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Player(models.Model):
	POSITION_TYPES = (
		('GOALKEEPER', 'Goalkeeper'),
		('DEFENDER', 'Defender'),
		('MIDFIELDER', 'Midfielder'),
		('STRIKER', 'Striker'),
	)
	name = models.CharField(
		max_length=100,
		unique=True)
	slug = models.SlugField(
		max_length=50,
		unique=True)
	squad_number = models.PositiveIntegerField()
	image = models.ImageField(
		upload_to='players')
	position = models.CharField(
		max_length=15,
		choices=POSITION_TYPES)
	club_appearances = models.PositiveIntegerField(
		blank=True,
		help_text='Total club appearances since joining the club.')
	goals = models.PositiveIntegerField(
		blank=True,
		null=True,
		help_text='Total goals since joining the club.')
	nationality = models.CharField(
		max_length=50,
		blank=True)
	yellow_cards = models.PositiveIntegerField(
		blank=True,
		null=True,
		help_text='Total yellow cards since joining the club.')
	red_cards = models.PositiveIntegerField(
		blank=True,
		null=True,
		help_text='Total red cards since joining the club.')
	date_of_birth = models.DateField(
		blank=True,
		null=True)
	height = models.CharField(
		max_length=10,
		blank=True,
		help_text='Height in cm.')
	weight = models.CharField(
		max_length=10,
		blank=True,
		help_text='Weight in kg.')
	previous_clubs = models.CharField(
		max_length=255,
		blank=True)
	biography = RichTextField()
	active = models.BooleanField(
		default=True,
		help_text='Uncheck this if the Player is no longer with the club.')

	class Meta:
		ordering = ['squad_number']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('player_detail',
			kwargs={'player_slug': self.slug})


class Photo(models.Model):
	image = ProcessedImageField(
        upload_to="gallery",
        processors = [ResizeToFill(750, 400)],
        format = 'JPEG',
        options = {'quality': 100})
	caption = models.CharField(
		max_length=50)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.caption


@python_2_unicode_compatible
class ClubHonor(models.Model):
	year = models.PositiveIntegerField()
	achievement = models.CharField(
		max_length=100)

	class Meta:
		ordering = ['-year']

	def __str__(self):
		return self.achievement


class AboutManager(models.Manager):
	def get_about(self):
		about = self.all()
		if about:
		    return about[0]
		return None

@python_2_unicode_compatible
class About(models.Model):
	content = RichTextField()
	objects = AboutManager()

	class Meta:
		verbose_name_plural = "About Us"

	def __str__(self):
		return "About Us"

	def save(self, *args, **kwargs):
	    """There should not be more than one About object."""
	    if About.objects.count() == 1 and not self.id:
	        raise Exception('Only one About Page object is allowed. Edit the existing About Page')
	    super(About, self).save(*args, **kwargs)


@python_2_unicode_compatible
class YoutubeVideo(models.Model):
	title = models.CharField(
		max_length=200)
	embed_link = models.TextField()

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.title


@python_2_unicode_compatible
class Statistic(models.Model):
	player = models.OneToOneField(
		Player)
	appearances = models.PositiveIntegerField(
		default=0,
		help_text='Total appearances in a season.')
	goals = models.PositiveIntegerField(
		default=0,
		help_text='Total goals in a season.')
	yellow_cards = models.PositiveIntegerField(
		default=0,
		help_text='Total yellow cards in a season.')
	red_cards = models.PositiveIntegerField(
		default=0,
		help_text='Total red cards in a season.')
	active = models.BooleanField(
		default=True,
		help_text='Uncheck this if the player is no longer with the club.')

	def __str__(self):
		return "%s's Stat" % self.player.name

	class Meta:
		ordering = ['player']


	def save(self, *args, **kwargs):
		if self.player.active == False:
			self.active = False
		else:
			self.active = True
		super(Statistic, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Sponsor(models.Model):
	name = models.CharField(
		max_length=100,
		unique=True)
	logo = models.ImageField(
		upload_to='sponsors')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-id']


@python_2_unicode_compatible
class ClubIndex(models.Model):
    club = models.ForeignKey(
        Club)
    played = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    loss = models.PositiveIntegerField()
    goals_for = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    goals_difference = models.IntegerField()
    points = models.PositiveIntegerField()

    def __str__(self):
        return "For: %s" % self.club.name

    class Meta:
    	verbose_name = 'Club Rank'
        verbose_name_plural = 'Club Ranks'
        ordering = ['-points', '-goals_difference', '-goals_for', 'club']


