from cinema.views import (
    add_cinema_view,
    add_showtime_view,
    cancel_showtime_view,
    list_all_showtimes_view,
    list_reserved_seats_view,
    list_showtime_seats,
    list_showtimes_view,
    reserve_showtime_view,
)

app_name = "cinema"

cinema_urls = {
    "add-cinema/": add_cinema_view,
    "add-showtime/": add_showtime_view,
    "showtimes/": list_all_showtimes_view,
    "showtimes/{user_id}/": list_showtimes_view,
    "showtime-seats/{showtime_id}/": list_showtime_seats,
    "reserve/{user_id}/{showtime_seat_id}/": reserve_showtime_view,
    "cancel/{user_id}/{showtime_seat_id}/": cancel_showtime_view,
    "reserved-seats/{user_id}/": list_reserved_seats_view,
}
