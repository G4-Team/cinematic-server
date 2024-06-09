from movie.views import add_movie_view

app_name = "movie"

movie_urls = {
    "add/": add_movie_view,
    "review/add/{movie_id}/": None,
    "comment/add/{movie_id}/{review_id}/": None,
}
