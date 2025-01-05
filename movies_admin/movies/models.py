import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.genre_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class ContentType(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField('creation_date')
    file_path = models.CharField('file_path', max_length=255)
    rating = models.FloatField('rating', blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(max_length=255, choices=ContentType.choices, default=ContentType.MOVIE)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_work')
        verbose_name_plural = _('film_works')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work_id = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            UniqueConstraint(fields=['film_work_id', 'genre_id'], name='unique_genre_film_work')]

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full_name', max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    class RoleChoices(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    film_work_id = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', choices=RoleChoices.choices, default=RoleChoices.ACTOR)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
