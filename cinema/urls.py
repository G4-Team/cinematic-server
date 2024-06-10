from cinema.views import *


app_name = 'cinema'

cinema_urls = {
    'add-cinema/': add_cinema_view,
    'add-showtime/': add_showtime_view,
    'movie-showtimes/{movie_id}': list_movie_showtimes_view,
    'cinema-showtimes/{cinema_id}': list_cinema_showtimes_view,
}
