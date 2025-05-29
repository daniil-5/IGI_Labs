import requests
import logging
from Django_Lab5.config import TMDB_API_KEY, OPENWEATHER_API_KEY, OMDB_API_KEY, DEFAULT_WEATHER_CITY, LOG_LEVEL

logger = logging.getLogger("cinema")

def get_tmdb_movies(api_key=None):

    if not api_key:
        api_key = TMDB_API_KEY

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1",
            timeout=5
        )

        if response.status_code == 200:
            movie_data = response.json()
            if 'results' in movie_data and movie_data['results']:
                movies = movie_data['results'][:5]
                logger.info(f"Successfully fetched {len(movies)} movies from TMDB API")
                return movies
            else:
                logger.warning("TMDB API returned no results")
                return None
        else:
            logger.error(f"TMDB API Error: Status code {response.status_code}")
            return None

    except requests.RequestException as e:
        logger.error(f"TMDB API Request Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error with TMDB API: {e}")
        return None

def get_weather_data(city=None, api_key=None):
    if not city:
        city = DEFAULT_WEATHER_CITY
    if not api_key:
        api_key = OPENWEATHER_API_KEY

    if not api_key:
        logger.error("No OpenWeather API key provided")
        return None

    try:
        logger.info(f"Fetching weather data for {city}")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            if 'main' in data and 'weather' in data and len(data['weather']) > 0:
                weather = {
                    'city': city,
                    'temperature': round(data['main']['temp'], 1),
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                logger.info(
                    f"Successfully retrieved weather data for {city}: {weather['temperature']}°C, {weather['description']}")
                return weather
            else:
                logger.error(f"Incomplete data received from OpenWeather API: {data}")
                return None
        else:
            error_message = f"OpenWeather API Error: Status code {response.status_code}"

            if response.status_code == 401:
                error_message += " - Invalid API key or unauthorized access"
            elif response.status_code == 404:
                error_message += f" - City '{city}' not found"
            elif response.status_code == 429:
                error_message += " - Rate limit exceeded"

            logger.error(error_message)

            try:
                error_data = response.json()
                if 'message' in error_data:
                    logger.error(f"API error message: {error_data['message']}")
            except:
                pass

            return None

    except requests.exceptions.Timeout:
        logger.error(f"OpenWeather API request timeout for {city}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error when accessing OpenWeather API for {city}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error when accessing OpenWeather API: {str(e)}")
        return None

def search_film_by_title(title, year, api_key=None):
    """
    Search for a film by title using TMDB API
    """
    if not api_key:
        api_key = TMDB_API_KEY

    try:
        search_response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}&year={year}",
            timeout=5
        )

        if search_response.status_code == 200:
            search_data = search_response.json()
            if 'results' in search_data and len(search_data['results']) > 0:
                tmdb_id = search_data['results'][0]['id']
                logger.info(f"Found TMDB ID {tmdb_id} for film '{title}'")
                return tmdb_id
            else:
                logger.warning(f"No TMDB results found for film '{title}'")
                return None
        else:
            logger.error(f"TMDB Search API Error: Status code {search_response.status_code}")
            return None

    except requests.RequestException as e:
        logger.error(f"TMDB API Request Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error with TMDB API: {e}")
        return None

def get_similar_films(tmdb_id, api_key=None):
    """
    Get similar films using TMDB API
    """
    if not api_key:
        api_key = TMDB_API_KEY

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}/similar",
            params={
                'api_key': api_key,
                'language': 'en-US',
                'page': 1
            },
            timeout=5
        )

        if response.status_code == 200:
            similar_data = response.json()
            if similar_data.get('results'):
                similar_films = similar_data['results'][:5]
                logger.info(f"Fetched {len(similar_films)} similar films for ID {tmdb_id}")
                return similar_films
            else:
                logger.warning(f"No similar films for TMDB ID {tmdb_id}")
                return None
        else:
            logger.error(f"TMDB Similar API Error: Status code {response.status_code}")
            return None

    except requests.RequestException as e:
        logger.error(f"TMDB API Request Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error with TMDB API: {e}")
        return None

def get_film_details_omdb(title, year, api_key=None):
    """
    Get detailed film information from OMDB API
    """
    if not api_key:
        api_key = OMDB_API_KEY

    try:
        omdb_response = requests.get(
            f"http://www.omdbapi.com/?apikey={api_key}&t={title}&y={year}",
            timeout=5
        )

        if omdb_response.status_code == 200:
            omdb_data = omdb_response.json()
            if omdb_data.get('Response') == 'True':
                film_info = {
                    'director': omdb_data.get('Director', 'Unknown'),
                    'actors': omdb_data.get('Actors', 'Unknown'),
                    'awards': omdb_data.get('Awards', 'None'),
                    'imdb_rating': omdb_data.get('imdbRating', 'N/A'),
                    'box_office': omdb_data.get('BoxOffice', 'N/A')
                }
                logger.info(f"Successfully fetched OMDB data for '{title}'")
                return film_info
            else:
                logger.warning(f"OMDB API found no results for '{title}': {omdb_data.get('Error', 'Unknown error')}")
                return None
        else:
            logger.error(f"OMDB API Error: Status code {omdb_response.status_code}")
            return None

    except requests.RequestException as e:
        logger.error(f"OMDB API Request Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error with OMDB API: {e}")
        return None
