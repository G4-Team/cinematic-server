from cinema.views import *


app_name = 'cinema'

cinema_urls = {
    'add-cinema/': add_cinema_view,
    'add-showtime/': add_showtime_view,
    'showtimes/' : list_showtime,
    'movie-showtimes/{movie_id}': list_movie_showtimes_view,
    'cinema-showtimes/{cinema_id}': list_cinema_showtimes_view,
    'showtime-seats/{showtime_id}': list_showtime_seats,
    'reserve/{user_id}/{showtime_id}': reserve_showtime_view,
    'cancel/{user_id}/{showtime_id}': cancel_showtime_view
}
