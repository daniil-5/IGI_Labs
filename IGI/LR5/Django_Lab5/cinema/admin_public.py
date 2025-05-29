from django.urls import path
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.shortcuts import render
from .models import Film, Genre, Country, ShowTime, Review, CinemaHall, Discount, Customer, Ticket



class PublicAdminSite(AdminSite):
    site_header = "Cinema Public View"
    site_title = "Cinema Films"
    index_title = "Film Catalog"

    def has_permission(self, request):
        return request.user.is_active

    def has_module_permission(self, request, app_label=None):
        return request.user.is_active

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)

        if request.user.is_authenticated and request.user.is_superuser:
            from django.shortcuts import redirect
            return redirect('/admin/')

        return response

    def logout(self, request, extra_context=None):
        from django.contrib.auth import logout
        from django.shortcuts import redirect
        logout(request)
        return redirect('/public/')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('portal/', self.admin_view(self.portal_view), name='portal'),
            path('stats/', self.admin_view(self.stats_view), name='stats'),
        ]
        return custom_urls + urls

    def portal_view(self, request):
        """Portal view for public site"""
        context = {
            'title': 'Cinema Public Portal',
            **self.each_context(request),
        }
        return render(request, 'public/index.html', context)

    def stats_view(self, request):
        """Stats view for public site"""
        context = {
            'title': 'Public Statistics',
            **self.each_context(request),
        }
        return render(request, 'public/index.html', context)

class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return request.user.is_active

public_site = PublicAdminSite(name='public_admin')


@admin.register(Film, site=public_site)
class FilmPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('title', 'display_genres', 'country', 'duration', 'release_year', 'age_restriction')
    list_filter = ('genres', 'country', 'release_year', 'age_restriction')
    search_fields = ('title', 'original_title', 'plot', 'description')
    readonly_fields = ('title', 'original_title', 'genres', 'country', 'duration',
                       'release_year', 'plot', 'description', 'poster',
                       'age_restriction', 'created_at', 'updated_at')

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Genres'


@admin.register(Genre, site=public_site)
class GenrePublicAdmin(ReadOnlyModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    readonly_fields = ('name', 'description')


@admin.register(Country, site=public_site)
class CountryPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('name',)


@admin.register(ShowTime, site=public_site)
class ShowTimePublicAdmin(ReadOnlyModelAdmin):
    list_display = ('film', 'hall', 'start_time', 'end_time', 'price')
    list_filter = ('hall', 'start_time', 'film')
    search_fields = ('film__title', 'hall__name')
    date_hierarchy = 'start_time'
    readonly_fields = ('film', 'hall', 'start_time', 'end_time', 'price')


@admin.register(Review, site=public_site)
class ReviewPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('film', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('film__title', 'user__username', 'text')
    readonly_fields = ('film', 'user', 'text', 'rating', 'created_at')


@admin.register(CinemaHall, site=public_site)
class CinemaHallPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('name', 'capacity', 'description')
    search_fields = ('name',)
    readonly_fields = ('name', 'capacity', 'description')


@admin.register(Discount, site=public_site)
class DiscountPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('name', 'percentage', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('percentage', 'valid_from', 'valid_to')
    search_fields = ('name', 'description')
    readonly_fields = ('name', 'description', 'percentage', 'valid_from', 'valid_to')


@admin.register(Customer, site=public_site)
class CustomerPublicAdmin(ReadOnlyModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date', 'age')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('user', 'phone_number', 'birth_date', 'age')

