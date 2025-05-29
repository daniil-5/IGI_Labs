# Run this with: python manage.py shell < create_news_data.py

from cinema.models import News
from django.utils import timezone
import datetime

# Clear existing news data
News.objects.all().delete()

# Create news items with updated image URLs
news_items = [
    {
        'title': 'New IMAX Screen Opening Next Month',
        'date': datetime.date(2025, 5, 15),
        'short_text': 'We are excited to announce the opening of our new IMAX screen with Dolby Atmos sound system.',
        'full_text': 'We are excited to announce the opening of our new IMAX screen with Dolby Atmos sound system. This state-of-the-art cinema hall will offer an unparalleled viewing experience with crystal clear 4K projection and immersive sound. The grand opening is scheduled for June 15, 2025, featuring the premiere of the most anticipated blockbuster of the summer.',
        'image_url': 'https://placehold.co/600x400?text=IMAX+Screen'
    },
    {
        'title': 'Summer Film Festival Announced',
        'date': datetime.date(2025, 5, 10),
        'short_text': 'Join us for a two-week celebration of classic cinema with daily screenings of award-winning films.',
        'full_text': 'Join us for a two-week celebration of classic cinema with daily screenings of award-winning films from the golden age of Hollywood to modern masterpieces. The festival will run from July 5-19, 2025, featuring panel discussions with film critics and special behind-the-scenes exhibits. Early bird tickets are now available with a 20% discount until June 1.',
        'image_url': 'https://placehold.co/600x400?text=Film+Festival'
    },
    {
        'title': 'Family Discount Packages Introduced',
        'date': datetime.date(2025, 5, 1),
        'short_text': 'New family packages make movie outings more affordable with special pricing for groups of 4 or more.',
        'full_text': 'We\'re introducing new family discount packages to make movie outings more affordable for everyone. Groups of 4 or more can enjoy special pricing that includes tickets, popcorn, and drinks. These packages are available for all screenings before 6 PM and all day on weekends. Book online to secure your family\'s spots for the upcoming animated features and family films.',
        'image_url': 'https://placehold.co/600x400?text=Family+Tickets'
    },
    {
        'title': 'Renovation of Hall 3 Completed',
        'date': datetime.date(2025, 4, 20),
        'short_text': 'We have completed the renovation of Cinema Hall 3 with new reclining seats and upgraded sound system.',
        'full_text': 'The renovation of Cinema Hall 3 has been completed ahead of schedule. The upgraded hall now features luxury reclining seats with extra legroom, cup holders, and adjustable headrests. The sound system has been upgraded to Dolby Atmos, and the projection system now supports high frame rate content. Come experience your favorite films in unprecedented comfort.',
        'image_url': 'https://placehold.co/600x400?text=Renovated+Hall'
    },
    {
        'title': 'Special Midnight Screenings for Horror Fans',
        'date': datetime.date(2025, 6, 1),
        'short_text': 'Monthly late-night horror movie marathons starting this July!',
        'full_text': 'Starting July 2025, we\'ll be hosting monthly midnight horror movie marathons. Experience classic horror films on the big screen with our premium sound system. Each event will feature 3 back-to-back cult classics with themed snacks and drinks. Costume contests with great prizes!',
        'image_url': 'https://placehold.co/600x400?text=Horror+Night'
    },
    {
        'title': 'Exclusive Partnership with Marvel Studios',
        'date': datetime.date(2025, 4, 15),
        'short_text': 'Early access screenings for all upcoming Marvel movies!',
        'full_text': 'We\'re proud to announce an exclusive partnership with Marvel Studios. Our cinema will host early access screenings for all upcoming Marvel Cinematic Universe releases. Marvel fans can enjoy special merchandise stands and exclusive collectibles available only at our venue.',
        'image_url': 'https://placehold.co/600x400?text=Marvel+Event'
    },
    {
        'title': 'Cinema Wins Best Venue Award 2025',
        'date': datetime.date(2025, 5, 5),
        'short_text': 'Voted best cinema experience in the region for third consecutive year.',
        'full_text': 'We\'re honored to receive the "Best Cinema Experience" award for the third year running. This recognition comes thanks to our continuous improvements in customer service, technical upgrades, and diverse programming. Thank you to all our loyal customers for your support!',
        'image_url': 'https://placehold.co/600x400?text=Award+Winner'
    },
    {
        'title': 'New VIP Membership Program',
        'date': datetime.date(2025, 4, 25),
        'short_text': 'Exclusive benefits for VIP members including priority booking and lounge access.',
        'full_text': 'Introducing our new VIP membership program with premium benefits: early ticket access, private lounge with complimentary snacks, dedicated concession lines, and 10% discount on all purchases. Three membership tiers available to suit different needs.',
        'image_url': 'https://placehold.co/600x400?text=VIP+Membership'
    },
    {
        'title': 'Holiday Movie Marathon Announcement',
        'date': datetime.date(2025, 4, 10),
        'short_text': '24-hour holiday movie marathon coming this December!',
        'full_text': 'Get ready for our annual 24-hour holiday movie marathon! Starting December 24th at 6 AM, enjoy back-to-back holiday classics with all-day breakfast menu and special holiday-themed cocktails. Wear your ugliest holiday sweater for a chance to win free tickets!',
        'image_url': 'https://placehold.co/600x400?text=Holiday+Movies'
    },
    {
        'title': 'New 4DX Screen Installation',
        'date': datetime.date(2025, 5, 20),
        'short_text': 'Experience movies with motion seats and environmental effects!',
        'full_text': 'We\'re installing our first 4DX screen featuring motion-activated seats, wind, mist, and scent effects. The new system will debut with the release of "Star Wars: New Horizons" in August 2025. Pre-book now for this immersive cinematic experience!',
        'image_url': 'https://placehold.co/600x400?text=4DX+Screen'
    },

]

for item in news_items:
    News.objects.create(**item)

print(f"{len(news_items)} news items created successfully!")