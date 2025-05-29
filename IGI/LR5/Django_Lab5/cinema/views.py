import calendar
import statistics
from time import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from Django_Lab5.config import DEFAULT_WEATHER_CITY
from cinema.models import Film, Review, Genre, Ticket, Customer, News, ShowTime
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .api_services import get_tmdb_movies, get_weather_data
from .chart_utils import generate_all_charts
from .forms import LoginForm, CustomerRegistrationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

def smart_redirect(request):
    """
    Redirect users based on their superuser status:
    - Superusers go to admin interface
    - Regular users go to public interface
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin/')
        else:
            return redirect('public/')
    else:
        return redirect('public/')
def welcome_page(request):
    # Get current date and time
    current_date = timezone.localtime(timezone.now())

    # Format the current date and time
    formatted_datetime = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    # Current user information
    current_user = f"{request.user.username}" if request.user.is_authenticated else "Guest"

    # Get featured films (first 3)
    featured_films = Film.objects.all()[:3]

    # Get the latest review
    latest_review = Review.objects.order_by('-created_at').first()

    # Get all films with filtering
    films = Film.objects.all()

    # Handle filtering
    title_query = request.GET.get('title', '')
    genre_query = request.GET.get('genre', '')
    duration_min = request.GET.get('duration_min', '')
    duration_max = request.GET.get('duration_max', '')

    if title_query:
        films = films.filter(Q(title__icontains=title_query) | Q(description__icontains=title_query))

    if genre_query:
        # Updated to use ManyToMany relationship correctly
        films = films.filter(genres__name=genre_query).distinct()

    if duration_min:
        films = films.filter(duration__gte=int(duration_min))

    if duration_max:
        films = films.filter(duration__lte=int(duration_max))

    # Get all available genres for the filter dropdown from the Genre model
    all_genres = Genre.objects.values_list('name', flat=True)

    context = {
        'current_date': current_date,
        'featured_films': featured_films,
        'latest_review': latest_review,
        'current_user': current_user,
        'formatted_datetime': formatted_datetime,
        'films': films,
        'all_genres': all_genres,
        'title_query': title_query,
        'genre_query': genre_query,
        'duration_min': duration_min,
        'duration_max': duration_max
    }

    return render(request, 'cinema/index.html', context)

@login_required
def add_review(request, film_id):
    if request.method == 'POST':
        film = get_object_or_404(Film, id=film_id)
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        # Check if user already has a review for this film
        existing_review = Review.objects.filter(film=film, user=request.user).first()

        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.text = text
            existing_review.save()
            # Use django.contrib.messages, not django.core.checks.messages
            from django.contrib import messages
            messages.success(request, 'Your review has been updated!')
        else:
            # Create new review
            review = Review(
                film=film,
                user=request.user,
                rating=rating,
                text=text,
                created_at=timezone.now()
            )
            review.save()
            from django.contrib import messages
            messages.success(request, 'Your review has been added!')

    # Remove the namespace here
    return redirect('film_detail', film_id=film_id)

def delete_review(request, film_id):
    if request.method == 'POST':
        film = get_object_or_404(Film, id=film_id)
        review = get_object_or_404(Review, film=film, user=request.user)
        review.delete()
        messages.success(request, 'Your review has been deleted!')

    return redirect('film_detail', film_id=film_id)

def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    reviews = Review.objects.filter(film=film).order_by('-created_at')
    user_review = reviews.filter(user=request.user).first() if request.user.is_authenticated else None

    return render(request, 'cinema/film_detail.html', {
        'film': film,
        'reviews': reviews,
        'user_review': user_review
    })

def about_page(request):
    return render(request, 'cinema/about.html')

def privacy_page(request):
    return render(request, 'cinema/privacy.html')

@login_required
def stats_view(request):
    """
    View for displaying statistics and charts
    """
    total_films = Film.objects.count()
    total_customers = Customer.objects.count()
    total_tickets = Ticket.objects.count()

    # Calculate revenue
    tickets = Ticket.objects.all()
    total_revenue = sum(float(ticket.final_price) for ticket in tickets) if tickets.exists() else 0

    if tickets.exists():
        prices = [float(ticket.final_price) for ticket in tickets]
        avg_ticket_price = statistics.mean(prices)
        median_ticket_price = statistics.median(prices)
    else:
        avg_ticket_price = 0
        median_ticket_price = 0

    # Calculate customer age statistics
    customers = Customer.objects.all()
    if customers.exists():
        ages = [customer.age for customer in customers]
        avg_customer_age = statistics.mean(ages)
        customers_alphabetical = customers.order_by('user__username')
    else:
        avg_customer_age = 0
        customers_alphabetical = []

    # Find most popular genre
    genre_ticket_counts = {}
    for ticket in tickets:
        film_genres = ticket.showtime.film.genres.all()
        for genre in film_genres:
            if genre.name in genre_ticket_counts:
                genre_ticket_counts[genre.name] += 1
            else:
                genre_ticket_counts[genre.name] = 1

    if genre_ticket_counts:
        most_popular_genre = max(genre_ticket_counts.items(), key=lambda x: x[1])[0]
    else:
        most_popular_genre = "N/A"

    charts = generate_all_charts()

    # Use the exact date and username requested
    current_datetime = "2025-05-27 16:56:00"
    current_username = "daniil-5"

    context = {
        'total_films': total_films,
        'total_customers': total_customers,
        'total_tickets': total_tickets,
        'total_revenue': total_revenue,
        'avg_ticket_price': avg_ticket_price,
        'median_ticket_price': median_ticket_price,
        'avg_customer_age': avg_customer_age,
        'most_popular_genre': most_popular_genre,
        'customers_alphabetical': customers_alphabetical,
        'charts': charts,
        'title': 'Statistics Dashboard',
        'current_datetime': current_datetime,
        'current_username': current_username,
    }

    return render(request, 'cinema/stats.html', context)


@login_required
def portal_view(request):
    """
    Standalone view for displaying the portal dashboard
    """
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
    }

    return render(request, 'cinema/portal.html', context)

def news_page(request):

    news_items = News.objects.filter(is_published=True).order_by('-date')

    return render(request, 'cinema/news.html', {
        'news_items': news_items
    })

def vacancies_page(request):
    formatted_datetime = timezone.localtime(timezone.now()).strftime('%Y/%m/%d %H:%M:%S')

    # Current user information
    current_user = f"{request.user.username}" if request.user.is_authenticated else "Guest"

    vacancies = [
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Projectionist',
            'department': 'Technical',
            'location': 'All Branches',
            'type': 'Full-time / Part-time',
            'posted_date': '2025-05-18',
            'description': 'Join our technical team as a Projectionist responsible for operating and maintaining digital projection systems and ensuring high-quality movie screenings.',
            'responsibilities': [
                'Set up and operate digital projection equipment',
                'Perform quality checks before screenings',
                'Troubleshoot and resolve technical issues promptly',
                'Maintain projection equipment in optimal condition',
                'Coordinate with management for screening schedules',
                'Ensure proper aspect ratios and sound levels for each screening'
            ],
            'requirements': [
                'Technical knowledge of digital projection systems',
                'Experience with cinema projection equipment preferred',
                'Basic computer skills and troubleshooting abilities',
                'Attention to detail and commitment to quality',
                'Ability to work evenings, weekends and holidays',
                'Technical certification or relevant experience preferred'
            ]
        },
        {
            'title': 'Concessions Attendant',
            'department': 'Food & Beverage',
            'location': 'All Branches',
            'type': 'Part-time',
            'posted_date': '2025-05-15',
            'description': 'We are hiring friendly and energetic Concessions Attendants to prepare and serve food and beverages to our cinema guests.',
            'responsibilities': [
                'Prepare and serve popcorn, beverages, and other concession items',
                'Process customer orders and handle cash transactions',
                'Maintain cleanliness of the concession area',
                'Stock inventory and report shortages',
                'Provide friendly and efficient customer service',
                'Assist with special events and promotions'
            ],
            'requirements': [
                'Customer service orientation and friendly demeanor',
                'Basic math skills for handling transactions',
                'Ability to stand for extended periods',
                'Food handling experience preferred',
                'Flexibility to work evenings, weekends and holidays',
                'No formal education requirements'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        },
        {
            'title': 'Cinema Manager',
            'department': 'Management',
            'location': 'Main Branch - Minsk',
            'type': 'Full-time',
            'posted_date': '2025-05-20',
            'description': 'We are looking for an experienced Cinema Manager to oversee daily operations, staff management, and customer service excellence at our main cinema complex.',
            'responsibilities': [
                'Manage daily operations of the cinema complex',
                'Supervise and train staff members',
                'Ensure excellent customer service standards',
                'Handle customer inquiries and resolve issues promptly',
                'Manage inventory and supplies for concessions',
                'Coordinate with film distributors and schedule screenings',
                'Implement marketing initiatives to increase attendance'
            ],
            'requirements': [
                'Previous experience in cinema or entertainment venue management',
                'Strong leadership and team management skills',
                'Excellent customer service orientation',
                'Flexibility to work evenings, weekends and holidays',
                'Knowledge of film industry trends and audience preferences',
                'Degree in Business Management or related field preferred'
            ]
        }
    ]

    return render(request, 'cinema/vacancies.html', {
        'formatted_datetime': formatted_datetime,
        'current_user': current_user,
        'vacancies': vacancies
    })


def qa_page(request):
    formatted_datetime = timezone.localtime(timezone.now()).strftime('%Y/%m/%d %H:%M:%S')

    # Current user information
    current_user = f"{request.user.username}" if request.user.is_authenticated else "Guest"

    # Sample FAQ categories and questions
    faq_categories = [
        {
            'name': 'Билеты и бронирование',
            'questions': [
                {
                    'question': 'Как забронировать билеты онлайн?',
                    'answer': 'Вы можете забронировать билеты через наш сайт, выбрав фильм, сеанс и место. Оплата производится банковской картой. После оплаты вы получите электронный билет на указанный email.'
                },
                {
                    'question': 'Можно ли вернуть или обменять билет?',
                    'answer': 'Возврат билетов возможен не позднее, чем за 3 часа до начала сеанса. Для возврата обратитесь в кассу кинотеатра с документом, удостоверяющим личность, или через личный кабинет на сайте.'
                },
                {
                    'question': 'Как долго действует бронь?',
                    'answer': 'Бронирование билетов действует в течение 30 минут. Если в течение этого времени билеты не будут выкуплены, бронь автоматически аннулируется.'
                },
                {
                    'question': 'Есть ли скидки для студентов и пенсионеров?',
                    'answer': 'Да, у нас действуют специальные скидки для студентов (20%) и пенсионеров (25%) при предъявлении соответствующих документов. Скидки действуют в будние дни на все сеансы до 18:00.'
                }
            ]
        },
        {
            'name': 'Кинотеатр и услуги',
            'questions': [
                {
                    'question': 'Можно ли приносить свою еду и напитки?',
                    'answer': 'Правилами кинотеатра запрещено проносить в зал собственную еду и напитки. У нас работает кинобар, где вы можете приобрести попкорн, напитки и другие закуски.'
                },
                {
                    'question': 'Есть ли в кинотеатре VIP-залы?',
                    'answer': 'Да, в нашем кинотеатре есть 2 VIP-зала с комфортными креслами-реклайнерами, персональными столиками и возможностью заказа еды и напитков прямо в зал.'
                },
                {
                    'question': 'Работает ли кинотеатр в праздничные дни?',
                    'answer': 'Да, кинотеатр работает без выходных, включая все праздничные дни. В праздники возможны изменения в расписании сеансов, которые публикуются заранее на нашем сайте.'
                }
            ]
        },
        {
            'name': 'Технические вопросы',
            'questions': [
                {
                    'question': 'Какие технологии используются для показа фильмов?',
                    'answer': 'Все залы оснащены современными цифровыми проекторами с поддержкой формата 4K и звуковыми системами Dolby Atmos или Dolby Digital. Некоторые залы поддерживают технологию 3D.'
                },
                {
                    'question': 'Что делать, если возникли проблемы при онлайн-бронировании?',
                    'answer': 'При возникновении технических проблем обратитесь в службу поддержки по телефону +375 (29) 123-45-67 или напишите на email: support@cinema-star.by. Наши специалисты помогут решить проблему.'
                }
            ]
        },
        {
            'name': 'Программа лояльности',
            'questions': [
                {
                    'question': 'Как работает программа лояльности?',
                    'answer': 'Наша программа лояльности "Звездный зритель" позволяет накапливать баллы за каждый просмотр фильма. Баллы можно обменивать на билеты, попкорн или напитки. За каждые 100 рублей покупки начисляется 10 баллов.'
                },
                {
                    'question': 'Как получить карту лояльности?',
                    'answer': 'Карту лояльности можно получить бесплатно на кассе кинотеатра при покупке билета. Для активации карты необходимо зарегистрироваться на нашем сайте или через мобильное приложение.'
                },
                {
                    'question': 'Есть ли особые привилегии для постоянных зрителей?',
                    'answer': 'Да, при достижении определенного количества посещений вы получаете статус VIP-зрителя, который дает право на дополнительные скидки, приглашения на закрытые премьеры и специальные мероприятия.'
                }
            ]
        }
    ]

    return render(request, 'cinema/qa.html', {
        'formatted_datetime': formatted_datetime,
        'current_user': current_user,
        'faq_categories': faq_categories
    })

def my_tickets(request):
    # Get the customer associated with the current user
    try:
        customer = request.user.customer
    except:
        return redirect('welcome_page')  # Redirect if no customer profile exists

    # Get current date for comparison
    current_date = timezone.localtime(timezone.now())

    # Get active tickets (for future showtimes)
    active_tickets = Ticket.objects.filter(
        customer=customer,
        showtime__start_time__gt=current_date
    ).order_by('showtime__start_time')

    # Get past tickets (history)
    past_tickets = Ticket.objects.filter(
        customer=customer,
        showtime__start_time__lte=current_date
    ).order_by('-showtime__start_time')

    # Handle search and filters
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')

    if search_query:
        active_tickets = active_tickets.filter(
            Q(showtime__film__title__icontains=search_query) |
            Q(showtime__hall__name__icontains=search_query)
        )
        past_tickets = past_tickets.filter(
            Q(showtime__film__title__icontains=search_query) |
            Q(showtime__hall__name__icontains=search_query)
        )

    if filter_type == 'today':
        today = current_date.date()
        active_tickets = active_tickets.filter(showtime__start_time__date=today)
    elif filter_type == 'week':
        week_later = current_date + timezone.timedelta(days=7)
        active_tickets = active_tickets.filter(
            showtime__start_time__range=(current_date, week_later)
        )
    elif filter_type == 'month':
        month_later = current_date + timezone.timedelta(days=30)
        active_tickets = active_tickets.filter(
            showtime__start_time__range=(current_date, month_later)
        )

    # Count number of tickets
    active_count = active_tickets.count()
    past_count = past_tickets.count()
    total_count = active_count + past_count

    return render(request, 'cinema/my_tickets.html', {
        'active_tickets': active_tickets,
        'past_tickets': past_tickets,
        'active_count': active_count,
        'past_count': past_count,
        'total_count': total_count,
        'search_query': search_query,
        'filter_type': filter_type
    })

class CustomerLoginView(LoginView):
    form_class = LoginForm
    template_name = 'cinema/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatted_datetime'] = "2025-05-24 16:27:45"
        context['current_user'] = "daniil-5"
        return context

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Set session expiry to 0 if remember_me is False
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('welcome_page')  # Redirect to home page after login

class CustomerRegistrationView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'cinema/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatted_datetime'] = timezone.localtime(timezone.now()).strftime('%Y/%m/%d %H:%M:%S')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('welcome_page')  # Redirect to home page after registration


class CustomerLogoutView(LogoutView):
    next_page = reverse_lazy('welcome_page')  # Redirect to home page after logout

    def dispatch(self, request, *args, **kwargs):
        # Make sure we use POST for logout to protect against CSRF
        if request.method == 'GET':
            # Convert GET requests to POST for convenience
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

