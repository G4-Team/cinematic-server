from cinema.views import *


app_name = 'cinema'

cinema_urls = {
    'add-cinema/': add_cinema_view,
    'add-showtime/': add_showtime_view
}
