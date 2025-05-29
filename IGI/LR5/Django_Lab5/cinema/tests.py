from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime
from decimal import Decimal

from cinema.models import (
    Genre, Country, Film, Review, CinemaHall,
    ShowTime, Discount, Customer, Ticket
)


class GenreModelTest(TestCase):
    def test_genre_creation(self):
        genre = Genre.objects.create(name="Action", description="Action movies")
        self.assertEqual(str(genre), "Action")
        self.assertEqual(genre.description, "Action movies")


class CountryModelTest(TestCase):
    def test_country_creation(self):
        country = Country.objects.create(name="USA")
        self.assertEqual(str(country), "USA")
        self.assertEqual(Country._meta.verbose_name_plural, "Countries")


class FilmModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="USA")
        self.genre = Genre.objects.create(name="Action")
        self.film = Film.objects.create(
            title="Test Film",
            original_title="Original Test Film",
            country=self.country,
            duration=120,
            release_year=2023,
            plot="Test plot",
            description="Test description",
            age_restriction=16
        )
        self.film.genres.add(self.genre)

    def test_film_creation(self):
        self.assertEqual(str(self.film), "Test Film")
        self.assertEqual(self.film.duration, 120)
        self.assertEqual(self.film.release_year, 2023)
        self.assertEqual(self.film.genres.first(), self.genre)
        self.assertEqual(self.film.country, self.country)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.country = Country.objects.create(name="USA")
        self.film = Film.objects.create(
            title="Test Film",
            country=self.country,
            duration=120,
            release_year=2023,
            plot="Test plot",
            description="Test description"
        )
        self.review = Review.objects.create(
            film=self.film,
            user=self.user,
            text="Great film!",
            rating=5
        )

    def test_review_creation(self):
        self.assertEqual(str(self.review), f"Review for Test Film by testuser")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, "Great film!")


class ShowTimeModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="USA")
        self.film = Film.objects.create(
            title="Test Film",
            country=self.country,
            duration=120,
            release_year=2023,
            plot="Test plot",
            description="Test description"
        )
        self.hall = CinemaHall.objects.create(
            name="Hall 1",
            capacity=100,
            description="Main hall"
        )
        self.start_time = timezone.now() + datetime.timedelta(days=1)
        self.showtime = ShowTime.objects.create(
            film=self.film,
            hall=self.hall,
            start_time=self.start_time,
            price=Decimal("10.00")
        )

    def test_showtime_creation(self):
        self.assertEqual(self.showtime.film, self.film)
        self.assertEqual(self.showtime.hall, self.hall)
        # Test auto-calculation of end_time
        expected_end_time = self.start_time + datetime.timedelta(minutes=120)
        self.assertEqual(self.showtime.end_time, expected_end_time)


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create a customer with valid data
        self.birth_date = timezone.now().date() - datetime.timedelta(days=365 * 20)

    def test_customer_creation(self):
        customer = Customer.objects.create(
            user=self.user,
            phone_number="+375 (29) 123-45-67",
            birth_date=self.birth_date
        )
        self.assertEqual(str(customer), "testuser")
        self.assertEqual(customer.phone_number, "+375 (29) 123-45-67")
        self.assertEqual(customer.age, 19)

    def test_customer_validation_future_date(self):
        future_date = timezone.now().date() + datetime.timedelta(days=10)
        customer = Customer(
            user=self.user,
            phone_number="+375 (29) 123-45-67",
            birth_date=future_date
        )
        with self.assertRaises(ValidationError):
            customer.clean()

    def test_customer_validation_underage(self):
        underage_date = timezone.now().date() - datetime.timedelta(days=365 * 17)  # 17 years ago
        customer = Customer(
            user=self.user,
            phone_number="+375 (29) 123-45-67",
            birth_date=underage_date
        )
        with self.assertRaises(ValidationError):
            customer.clean()


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.birth_date = timezone.now().date() - datetime.timedelta(days=365 * 20)
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number="+375 (29) 123-45-67",
            birth_date=self.birth_date
        )
        self.country = Country.objects.create(name="USA")
        self.film = Film.objects.create(
            title="Test Film",
            country=self.country,
            duration=120,
            release_year=2023,
            plot="Test plot",
            description="Test description"
        )
        self.hall = CinemaHall.objects.create(
            name="Hall 1",
            capacity=100
        )
        self.start_time = timezone.now() + datetime.timedelta(days=1)
        self.showtime = ShowTime.objects.create(
            film=self.film,
            hall=self.hall,
            start_time=self.start_time,
            price=Decimal("10.00")
        )
        self.discount = Discount.objects.create(
            name="Student Discount",
            description="Discount for students",
            percentage=20,
            valid_from=timezone.now() - datetime.timedelta(days=10),
            valid_to=timezone.now() + datetime.timedelta(days=10)
        )
        self.ticket = Ticket.objects.create(
            showtime=self.showtime,
            customer=self.customer,
            seat_row=1,
            seat_number=5,
            discount=self.discount
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.showtime, self.showtime)
        self.assertEqual(self.ticket.customer, self.customer)
        self.assertEqual(self.ticket.seat_row, 1)
        self.assertEqual(self.ticket.seat_number, 5)
        self.assertEqual(self.ticket.discount, self.discount)

    def test_final_price_with_discount(self):
        # 10.00 with 20% discount = 8.00
        self.assertEqual(self.ticket.final_price, Decimal("8.00"))

    def test_final_price_without_discount(self):
        ticket = Ticket.objects.create(
            showtime=self.showtime,
            customer=self.customer,
            seat_row=1,
            seat_number=6
        )
        self.assertEqual(ticket.final_price, Decimal("10.00"))




