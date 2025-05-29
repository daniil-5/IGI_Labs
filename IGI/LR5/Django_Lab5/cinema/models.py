from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
import datetime
import logging

from Django_Lab5 import settings

logger = logging.getLogger('cinema')

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Genre created: {self.name}")
        else:
            logger.info(f"Genre updated: {self.name}")

    def delete(self, *args, **kwargs):
        logger.info(f"Genre deleted: {self.name}")
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Country created: {self.name}")
        else:
            logger.info(f"Country updated: {self.name}")

    def delete(self, *args, **kwargs):
        logger.info(f"Country deleted: {self.name}")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']


class Film(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre, related_name='films')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='films')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_year = models.PositiveIntegerField(validators=[MinValueValidator(1895)])
    plot = models.TextField()
    description = models.TextField()
    poster = models.ImageField(upload_to='film_posters/', blank=True, null=True)
    age_restriction = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Film created: {self.title} (ID: {self.pk})")
        else:
            logger.info(f"Film updated: {self.title} (ID: {self.pk})")

    def delete(self, *args, **kwargs):
        logger.info(f"Film deleted: {self.title} (ID: {self.pk})")
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.film.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Review created: ID {self.pk} for film '{self.film.title}' by user '{self.user.username}'")
        else:
            logger.info(f"Review updated: ID {self.pk} for film '{self.film.title}' by user '{self.user.username}'")

    def delete(self, *args, **kwargs):
        logger.info(f"Review deleted: ID {self.pk} for film '{self.film.title}' by user '{self.user.username}'")
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"CinemaHall created: {self.name} (ID: {self.pk})")
        else:
            logger.info(f"CinemaHall updated: {self.name} (ID: {self.pk})")

    def delete(self, *args, **kwargs):
        logger.info(f"CinemaHall deleted: {self.name} (ID: {self.pk})")
        super().delete(*args, **kwargs)


class ShowTime(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.film.title} - {self.start_time.strftime('%d/%m/%Y %H:%M')}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.end_time:
            # Calculate end time based on film duration
            self.end_time = self.start_time + datetime.timedelta(minutes=self.film.duration)

        super().save(*args, **kwargs)

        if is_new:
            logger.info(f"ShowTime created: ID {self.pk} for film '{self.film.title}' at {self.start_time}")
        else:
            logger.info(f"ShowTime updated: ID {self.pk} for film '{self.film.title}' at {self.start_time}")

    def delete(self, *args, **kwargs):
        logger.info(f"ShowTime deleted: ID {self.pk} for film '{self.film.title}' at {self.start_time}")
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['start_time']


class Discount(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Discount created: {self.name} (ID: {self.pk}) - {self.percentage}%")
        else:
            logger.info(f"Discount updated: {self.name} (ID: {self.pk}) - {self.percentage}%")

    def delete(self, *args, **kwargs):
        logger.info(f"Discount deleted: {self.name} (ID: {self.pk}) - {self.percentage}%")
        super().delete(*args, **kwargs)

    @property
    def is_active(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                message="Phone number must be entered in the format: '+375 (XX) XXX-XX-XX'"
            )
        ]
    )
    birth_date = models.DateField()

    def calculate_age(self, birth_date):
        if birth_date is None:
            return None
        from datetime import date
        if not isinstance(birth_date, date):
            try:
                birth_date = birth_date.date() if hasattr(birth_date, 'date') else date(birth_date)
            except (AttributeError, TypeError, ValueError):
                raise TypeError("Дата рождения должна быть объектом типа date")

        today = timezone.now().date()

        if birth_date > today:
            raise ValueError("Дата рождения не может быть в будущем")

        age = today.year - birth_date.year

        # Вычитаем 1, если день рождения в этом году ещё не наступил
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def clean(self):
        super().clean()
        if self.birth_date is None:
            raise ValidationError({'birth_date': 'Birth date is required.'})

        today = timezone.now().date()

        if self.birth_date > today:
            raise ValidationError({'birth_date': 'Birth date cannot be in the future.'})

        try:
            age = self.calculate_age(self.birth_date)
            if age < 18:
                raise ValidationError({'birth_date': 'Customers must be at least 18 years old.'})
        except (TypeError, ValueError) as e:
            raise ValidationError({'birth_date': str(e)})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.clean()
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Customer created: {self.user.username} (ID: {self.pk})")
        else:
            logger.info(f"Customer updated: {self.user.username} (ID: {self.pk})")

    def delete(self, *args, **kwargs):
        logger.info(f"Customer deleted: {self.user.username} (ID: {self.pk})")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Ticket(models.Model):
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='tickets')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    seat_row = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.showtime} - Row {self.seat_row}, Seat {self.seat_number}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        customer_info = f"for customer {self.customer.user.username}" if self.customer else "without customer"
        if is_new:
            logger.info(f"Ticket created: ID {self.pk} for film '{self.showtime.film.title}' at {self.showtime.start_time} {customer_info}")
        else:
            logger.info(f"Ticket updated: ID {self.pk} for film '{self.showtime.film.title}' at {self.showtime.start_time} {customer_info}")

    def delete(self, *args, **kwargs):
        customer_info = f"for customer {self.customer.user.username}" if self.customer else "without customer"
        logger.info(f"Ticket deleted: ID {self.pk} for film '{self.showtime.film.title}' at {self.showtime.start_time} {customer_info}")
        super().delete(*args, **kwargs)

    @property
    def final_price(self):
        from decimal import Decimal
        if self.discount:
            discount_factor = Decimal(1) - (Decimal(self.discount.percentage) / Decimal(100))
            return self.showtime.price * discount_factor
        return self.showtime.price

    class Meta:
        unique_together = ('showtime', 'seat_row', 'seat_number')


class News(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    short_text = models.TextField(max_length=255)
    full_text = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    image_url = models.URLField(max_length=255, blank=True,
                                help_text="URL to the news image (used if no image is uploaded)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            try:
                return self.image.url
            except ValueError:
                # Handle case where image field exists but file was deleted
                pass

        # Fallback to external URL if exists and not empty
        if self.image_url and self.image_url.strip():
            return self.image_url.strip()

        # Final fallback to static placeholder
        return f'{settings.STATIC_URL}cinema/images/news_placeholder.jpg'
