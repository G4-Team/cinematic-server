from movie.views import (
    add_comment_movie_review_view,
    add_movie_review_view,
    add_movie_view,
    list_movie_comments_view,
)

app_name = "movie"

movie_urls = {
    "add/": add_movie_view,
    "review/add/{user_id}/{movie_id}/": add_movie_review_view,
    "comment/add/{user_id}/{review_id}/": add_comment_movie_review_view,
    "comment/list/{movie_id}/": list_movie_comments_view,
}
