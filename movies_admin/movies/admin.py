from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person_id', 'role')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name', 'description')
    list_filter = ('genre_name', 'description')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    search_fields = ('title', 'description')
    list_display = ('title', 'get_genres', 'creation_date', 'rating')
    list_filter = ('title', 'short_description', 'creation_date', 'rating')

    def short_description(self, obj):
        return (obj.description[:50] + "...") if len(obj.description) > 50 else obj.description

    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join((genre.name for genre in obj.genres.all()))

    get_genres.short_description = 'Жанры фильма'

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    list_filter = ('full_name',)
    search_fields = ('full_name',)
