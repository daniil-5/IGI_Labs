import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Lab5.settings')
django.setup()

from django.contrib.auth.models import User
from cinema.models import Genre, Country, CinemaHall, Film, ShowTime, Discount, Customer, Review, Ticket

from django.utils import timezone
import datetime

# Create genres
genres = [
    {"name": "Action", "description": "Exciting action scenes"},
    {"name": "Comedy", "description": "Funny and humorous"},
    {"name": "Drama", "description": "Serious and dramatic"},
    {"name": "Horror", "description": "Scary and frightening"},
    {"name": "Science Fiction", "description": "Futuristic concepts"},
    {"name": "Romance", "description": "Love stories"},
    {"name": "Adventure", "description": "Exciting journeys and quests"},
    {"name": "Thriller", "description": "Suspenseful and thrilling"}
]

for genre_data in genres:
    Genre.objects.get_or_create(name=genre_data["name"], defaults=genre_data)

# Create countries
countries = ["USA", "UK", "France", "Germany", "Japan", "South Korea", "India", "Russia", "Canada", "Australia"]
for country_name in countries:
    Country.objects.get_or_create(name=country_name)

# Create cinema halls
halls = [
    {"name": "Hall 1", "capacity": 100, "description": "Standard hall"},
    {"name": "Hall 2", "capacity": 150, "description": "Large hall with premium seats"},
    {"name": "Hall 3", "capacity": 80, "description": "Intimate hall for art films"},
    {"name": "VIP Hall", "capacity": 50, "description": "Luxury experience"}
]

for hall_data in halls:
    CinemaHall.objects.get_or_create(name=hall_data["name"], defaults=hall_data)

# Create films if they don't exist
films_data = [
    {
        "title": "The Space Adventure",
        "original_title": "Space Adventure",
        "country_name": "USA",
        "duration": 125,
        "release_year": 2024,
        "plot": "A team of astronauts embarks on a dangerous mission to save humanity.",
        "description": "Epic science fiction movie about space exploration and human survival.",
        "age_restriction": 12,
        "genres": ["Science Fiction", "Action"]
    },
    {
        "title": "Laugh Out Loud",
        "country_name": "UK",
        "duration": 95,
        "release_year": 2023,
        "plot": "A series of hilarious events in the life of a comedian.",
        "description": "A comedy that will make you laugh from start to finish.",
        "age_restriction": 16,
        "genres": ["Comedy"]
    },
    {
        "title": "The Last Journey",
        "country_name": "France",
        "duration": 140,
        "release_year": 2025,
        "plot": "An emotional journey of self-discovery and redemption.",
        "description": "A touching drama about life's most important questions.",
        "age_restriction": 12,
        "genres": ["Drama"]
    },
    {
        "title": "Night Terror",
        "country_name": "USA",
        "duration": 105,
        "release_year": 2024,
        "plot": "A group of friends discover a haunted house with a dark secret.",
        "description": "A terrifying horror film that will keep you on the edge of your seat.",
        "age_restriction": 18,
        "genres": ["Horror", "Thriller"]
    },
    {
        "title": "Love in Paris",
        "country_name": "France",
        "duration": 110,
        "release_year": 2023,
        "plot": "Two strangers meet in Paris and fall in love over a weekend.",
        "description": "A beautiful romance set in the city of love.",
        "age_restriction": 12,
        "genres": ["Romance", "Drama"]
    },
    {
        "title": "The Quest for Treasure",
        "country_name": "UK",
        "duration": 135,
        "release_year": 2025,
        "plot": "An archaeologist searches for a legendary treasure in the Amazon rainforest.",
        "description": "An exciting adventure with action and mystery.",
        "age_restriction": 12,
        "genres": ["Adventure", "Action"]
    },
    {
        "title": "The Secret Agent",
        "country_name": "USA",
        "duration": 130,
        "release_year": 2024,
        "plot": "A spy must uncover a conspiracy within their own agency.",
        "description": "A thrilling espionage story with unexpected twists.",
        "age_restriction": 16,
        "genres": ["Thriller", "Action"]
    },
    {
        "title": "Family Vacation",
        "country_name": "USA",
        "duration": 100,
        "release_year": 2023,
        "plot": "A family road trip goes hilariously wrong.",
        "description": "A family-friendly comedy about the joys and challenges of travel.",
        "age_restriction": 6,
        "genres": ["Comedy", "Adventure"]
    },
    {
        "title": "The Last Samurai",
        "country_name": "Japan",
        "duration": 150,
        "release_year": 2024,
        "plot": "A warrior fights to preserve traditional values in a changing world.",
        "description": "An epic historical drama about honor and tradition.",
        "age_restriction": 14,
        "genres": ["Drama", "Action"]
    },
    {
        "title": "Future World",
        "country_name": "USA",
        "duration": 120,
        "release_year": 2025,
        "plot": "In a dystopian future, a rebel fights against an oppressive regime.",
        "description": "A thought-provoking science fiction film about freedom and control.",
        "age_restriction": 16,
        "genres": ["Science Fiction", "Action"]
    }
]

# Create films
for film_data in films_data:
    country = Country.objects.get(name=film_data["country_name"])

    # Extract and remove genres from film data
    genre_names = film_data.pop("genres")
    country_name = film_data.pop("country_name")

    # Create or get film
    film, created = Film.objects.get_or_create(
        title=film_data["title"],
        defaults={**film_data, "country": country}
    )

    # Add genres
    for genre_name in genre_names:
        genre = Genre.objects.get(name=genre_name)
        film.genres.add(genre)


# Create showtimes
def create_showtimes():
    # Get some films
    films = list(Film.objects.all())[:5]
    halls = list(CinemaHall.objects.all())

    # Start date (tomorrow)
    start_date = timezone.now() + datetime.timedelta(days=1)

    for i in range(10):  # Create 10 showtimes
        film = films[i % len(films)]
        hall = halls[i % len(halls)]
        start = start_date + datetime.timedelta(days=i // 2, hours=i * 2 % 12 + 10)

        ShowTime.objects.get_or_create(
            film=film,
            hall=hall,
            start_time=start,
            defaults={
                "price": 10.00 + (i % 5) * 2,  # Price between 10 and 18
                "end_time": start + datetime.timedelta(minutes=film.duration)
            }
        )


# Create discounts
def create_discounts():
    discounts = [
        {
            "name": "Student Discount",
            "description": "Special discount for students with valid ID",
            "percentage": 20,
            "valid_from": timezone.now() - datetime.timedelta(days=10),
            "valid_to": timezone.now() + datetime.timedelta(days=90)
        },
        {
            "name": "Senior Discount",
            "description": "Discount for seniors aged 65+",
            "percentage": 25,
            "valid_from": timezone.now() - datetime.timedelta(days=10),
            "valid_to": timezone.now() + datetime.timedelta(days=90)
        },
        {
            "name": "Early Bird Special",
            "description": "Special discount for morning shows before 12pm",
            "percentage": 15,
            "valid_from": timezone.now() - datetime.timedelta(days=10),
            "valid_to": timezone.now() + datetime.timedelta(days=60)
        },
        {
            "name": "Family Package",
            "description": "Discount for families with 3+ members",
            "percentage": 10,
            "valid_from": timezone.now() - datetime.timedelta(days=10),
            "valid_to": timezone.now() + datetime.timedelta(days=120)
        }
    ]

    for discount_data in discounts:
        Discount.objects.get_or_create(
            name=discount_data["name"],
            defaults=discount_data
        )


def create_users_and_customers():
    print("Creating users and customers...")

    # Customer data
    customers_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+375 (29) 123-45-67",
            "birth_date": timezone.now().date() - datetime.timedelta(days=365 * 25)  # 25 years old
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "password123",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+375 (33) 987-65-43",
            "birth_date": timezone.now().date() - datetime.timedelta(days=365 * 30)  # 30 years old
        },
        {
            "username": "alex_brown",
            "email": "alex@example.com",
            "password": "password123",
            "first_name": "Alex",
            "last_name": "Brown",
            "phone": "+375 (44) 555-77-88",
            "birth_date": timezone.now().date() - datetime.timedelta(days=365 * 22)  # 22 years old
        },
        {
            "username": "maria_garcia",
            "email": "maria@example.com",
            "password": "password123",
            "first_name": "Maria",
            "last_name": "Garcia",
            "phone": "+375 (25) 111-22-33",
            "birth_date": timezone.now().date() - datetime.timedelta(days=365 * 40)  # 40 years old
        },
    ]

    # Create users and customers
    for data in customers_data:
        user, user_created = User.objects.get_or_create(
            username=data["username"],
            defaults={
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"]
            }
        )

        if user_created:
            user.set_password(data["password"])
            user.save()
            print(f"Created user: {user.username}")

        # Create customer if it doesn't exist
        customer, customer_created = Customer.objects.get_or_create(
            user=user,
            defaults={
                "phone_number": data["phone"],
                "birth_date": data["birth_date"]
            }
        )

        if customer_created:
            print(f"Created customer for: {user.username}")
        else:
            print(f"Customer for {user.username} already exists")


import random


def create_reviews():
    print("Creating reviews...")

    # Get users and films
    users = User.objects.all()
    films = Film.objects.all()

    review_texts = [
        "Absolutely loved it! The plot was engaging and the characters were well-developed.",
        "Good film, but a bit too long. The middle part dragged a bit.",
        "Amazing cinematography and soundtrack. Highly recommended!",
        "Not what I expected, but still enjoyable. The acting was superb.",
        "A masterpiece! Will definitely watch again.",
        "Decent film but the storyline was somewhat predictable.",
        "Great special effects, but the dialogue needed improvement.",
        "One of the best films I've seen this year!",
    ]

    # Create reviews
    for film in films:
        # Add 2-4 reviews per film
        num_reviews = random.randint(2, 4)
        for i in range(num_reviews):
            user = random.choice(users)
            text = random.choice(review_texts)
            rating = random.randint(3, 5)  # Ratings between 3-5

            # Check if this user already reviewed this film
            if not Review.objects.filter(film=film, user=user).exists():
                Review.objects.create(
                    film=film,
                    user=user,
                    text=text,
                    rating=rating
                )
                print(f"Created review for '{film.title}' by {user.username}")


def create_tickets():
    print("Creating tickets...")

    # Get customers, showtimes, and discounts
    customers = Customer.objects.all()
    showtimes = ShowTime.objects.all()
    discounts = Discount.objects.all()

    # For each showtime, create some tickets
    for showtime in showtimes:
        # Create 5-15 tickets per showtime
        num_tickets = random.randint(5, min(15, showtime.hall.capacity))

        # Track seats to avoid duplicates
        booked_seats = set()

        for _ in range(num_tickets):
            # Choose a random customer
            customer = random.choice(customers)

            # Generate a unique seat
            while True:
                seat_row = random.randint(1, 10)  # Assuming 10 rows
                seat_number = random.randint(1, 10)  # Assuming 10 seats per row
                seat = (seat_row, seat_number)

                if seat not in booked_seats and not Ticket.objects.filter(
                        showtime=showtime, seat_row=seat_row, seat_number=seat_number).exists():
                    booked_seats.add(seat)
                    break

            # Randomly apply a discount (30% chance)
            discount = random.choice(discounts) if discounts and random.random() < 0.3 else None

            # Create the ticket
            Ticket.objects.create(
                showtime=showtime,
                customer=customer,
                seat_row=seat_row,
                seat_number=seat_number,
                discount=discount
            )

            print(f"Created ticket for '{showtime.film.title}' - Seat: Row {seat_row}, Number {seat_number}")

create_users_and_customers()
# create_showtimes()
# create_discounts()
create_reviews()
create_tickets()

print("Database populated successfully!")