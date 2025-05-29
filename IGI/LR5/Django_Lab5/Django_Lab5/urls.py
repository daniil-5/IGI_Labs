from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from cinema import views, admin
from cinema.admin_public import public_site
from cinema.admin import admin_site
from cinema.views import smart_redirect

urlpatterns = [
    re_path(r'^admin/', admin_site.urls),           # Custom admin site with charts
    re_path(r'^public/', public_site.urls),         # Public admin site (read-only)
    re_path(r'^login$', smart_redirect),
    re_path('^$', views.welcome_page, name='welcome_page'),
    path('about/', views.about_page, name='about'),
    path('privacy/', views.privacy_page, name='privacy'),
    path('news/', views.news_page, name='news'),
    path('vacancies/', views.vacancies_page, name='vacancies'),
    path('qa/', views.qa_page, name='qa'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('portal/', views.portal_view, name='portal'),
    path('stats/', views.stats_view, name='stats'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),
    path('film/<int:film_id>/add_review/', views.add_review, name='add_review'),
    path('film/<int:film_id>/delete_review/', views.delete_review, name='delete_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
