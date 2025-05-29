import calendar
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
import statistics
from .models import Genre, Country, Film, Review, CinemaHall, ShowTime, Discount, Customer, Ticket, News
from .chart_utils import generate_all_charts
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import logging
from Django_Lab5.config import DEFAULT_WEATHER_CITY
from cinema.api_services import get_tmdb_movies, get_weather_data
from django.utils import timezone


logger = logging.getLogger("cinema")

class CinemaAdminSite(admin.AdminSite):
    """
    Custom admin site for cinema application with statistics dashboard
    """
    site_header = "Cinema Administration"
    site_title = "Cinema Admin Portal"
    index_title = "Welcome to Cinema Admin Portal"

    def has_permission(self, request):
        return request.user.is_active

    def has_module_permission(self, request, app_label=None):
        return request.user.is_active

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)

        if request.user.is_authenticated and not request.user.is_superuser:
            from django.shortcuts import redirect
            return redirect('/public/')
        return response

    def logout(self, request, extra_context=None):
        """Override logout to ensure proper redirection after logout"""
        from django.contrib.auth import logout
        from django.shortcuts import redirect
        logout(request)
        return redirect('/admin/')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('portal/', self.admin_view(self.portal_view), name='portal'),
        ]
        return custom_urls + urls


    def portal_view(self, request):
        """
        View for displaying the original IndexView inside admin panel
        """
        logger.info("Portal view accessed by %s", request.user.username)

        # Featured films (newest releases)
        featured_films = Film.objects.all().order_by('-release_year')[:5]

        today = timezone.now().date()
        todays_showtimes = ShowTime.objects.filter(
            start_time__date=today
        ).order_by('start_time')

        current_date = timezone.localtime(timezone.now())
        # Get the current timezone name
        current_timezone = timezone.get_current_timezone_name()

        cal = calendar.monthcalendar(today.year, today.month)

        # API 1: TMDB API integration - movie news
        movie_news = get_tmdb_movies()

        # API 2: OpenWeather API integration - current weather
        weather = get_weather_data(city=DEFAULT_WEATHER_CITY)

        context = {
            'featured_films': featured_films,
            'todays_showtimes': todays_showtimes,
            'current_date': current_date,
            'current_timezone': current_timezone,
            'calendar': cal,
            'movie_news': movie_news,
            'weather': weather,

            'title': 'Cinema Portal',
            'site_title': self.site_title,
            'site_header': self.site_header,
            'has_permission': True,
            **self.each_context(request),
        }

        return render(request, 'admin/cinema/portal.html', context)


admin_site = CinemaAdminSite(name='cinema_admin')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'film_count')
    search_fields = ('name',)

    def film_count(self, obj):
        return obj.films.count()

    film_count.short_description = 'Number of films'

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'film_count')
    search_fields = ('name',)

    def film_count(self, obj):
        return obj.films.count()

    film_count.short_description = 'Number of films'

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'created_at')

class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genres', 'country', 'duration', 'release_year', 'age_restriction', 'created_at')
    list_filter = ('genres', 'country', 'release_year', 'age_restriction')
    search_fields = ('title', 'original_title', 'plot', 'description')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at', 'display_poster')
    inlines = [ReviewInline]

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Genres'

    def display_poster(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="300" />', obj.poster.url)
        return "No poster uploaded"

    display_poster.short_description = 'Poster Preview'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('film', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('film__title', 'user__username', 'text')
    readonly_fields = ('created_at',)

class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'description')
    search_fields = ('name',)

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0

class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ('film', 'hall', 'start_time', 'end_time', 'formatted_price', 'tickets_sold')
    list_filter = ('hall', 'start_time', 'film')
    search_fields = ('film__title', 'hall__name')
    date_hierarchy = 'start_time'
    inlines = [TicketInline]

    def tickets_sold(self, obj):
        return obj.tickets.count()

    tickets_sold.short_description = 'Tickets Sold'

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('percentage', 'valid_from', 'valid_to')
    search_fields = ('name', 'description')

class CustomerAdmin(admin.ModelAdmin):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'})
    )
    list_display = ('user', 'phone_number', 'birth_date', 'age')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('age',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'showtime', 'customer', 'seat_row', 'seat_number', 'final_price', 'purchase_date')
    list_filter = ('showtime__film', 'showtime__start_time', 'purchase_date')
    search_fields = ('customer__user__username', 'showtime__film__title')
    date_hierarchy = 'purchase_date'
    readonly_fields = ('purchase_date', 'final_price')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'short_text', 'full_text')
    date_hierarchy = 'date'

admin_site.register(News, NewsAdmin)
admin_site.register(Genre, GenreAdmin)
admin_site.register(Country, CountryAdmin)
admin_site.register(Film, FilmAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(CinemaHall, CinemaHallAdmin)
admin_site.register(ShowTime, ShowTimeAdmin)
admin_site.register(Discount, DiscountAdmin)
admin_site.register(Customer, CustomerAdmin)
admin_site.register(Ticket, TicketAdmin)
admin_site.register(User, UserAdmin)