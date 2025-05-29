import matplotlib.pyplot as plt
import matplotlib
import io
import base64
from django.db.models import Count
import logging
from .models import Film, Genre, Customer

matplotlib.use('Agg')
logger = logging.getLogger("cinema")

def get_base64_graph(plt):
    """
    Convert a matplotlib plot to a base64 encoded string for embedding in HTML
    """
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode('utf-8')
    return graph

def generate_genre_distribution_chart():
    """
    Generate a pie chart showing the distribution of films by genre
    """
    # Get genre counts
    logger.info('Generating genre distribution chart')
    genre_counts = Genre.objects.annotate(film_count=Count('films')).order_by('-film_count')
    
    # Name the data for chart
    labels = [genre.name for genre in genre_counts]
    sizes = [genre.film_count for genre in genre_counts]
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Ensures that pie is drawn as a circle
    plt.title('Distribution of Films by Genre')
    
    # Convert to base64
    graph = get_base64_graph(plt)
    plt.close()
    
    return graph

def generate_popular_films_chart():
    """
    Generate a bar chart showing the most popular films by ticket sales
    """
    logger.info('Generating popular films chart')
    film_tickets = Film.objects.annotate(
        tickets_sold=Count('showtimes__tickets')
    ).order_by('-tickets_sold')[:10]
    
    # Prepare data for chart
    films = [film.title for film in film_tickets]
    tickets = [film.tickets_sold for film in film_tickets]
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(films, tickets)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Films')
    plt.ylabel('Tickets Sold')
    plt.title('Most Popular Films by Ticket Sales')
    plt.tight_layout()

    graph = get_base64_graph(plt)
    plt.close()
    
    return graph

def generate_age_distribution_chart():
    """
    Generate a bar chart showing the distribution of customers by age group
    """
    logger.info('Generating age distribution chart')
    customers = Customer.objects.all()
    
    if not customers.exists():
        return None

    ages = [customer.age for customer in customers]

    age_groups = {
        '18-25': 0,
        '26-35': 0,
        '36-45': 0,
        '46-55': 0,
        '56+': 0
    }

    for age in ages:
        if 18 <= age <= 25:
            age_groups['18-25'] += 1
        elif 26 <= age <= 35:
            age_groups['26-35'] += 1
        elif 36 <= age <= 45:
            age_groups['36-45'] += 1
        elif 46 <= age <= 55:
            age_groups['46-55'] += 1
        else:
            age_groups['56+'] += 1

    plt.figure(figsize=(10, 6))
    plt.bar(age_groups.keys(), age_groups.values())
    plt.xlabel('Age Group')
    plt.ylabel('Number of Customers')
    plt.title('Distribution of Customers by Age Group')

    graph = get_base64_graph(plt)
    plt.close()
    
    return graph

def generate_all_charts():
    """
    Generate all charts and return them as a dictionary
    """
    logger.info('Generating all charts')
    charts = {
        'genre_distribution': generate_genre_distribution_chart(),
        'popular_films': generate_popular_films_chart(),
        'age_distribution': generate_age_distribution_chart()
    }
    
    return charts