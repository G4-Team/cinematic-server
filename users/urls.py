from users.views import add_user_view, get_user_view

app_name = "users"

users_urls = {
    "add/": add_user_view,
    "get/{id}/": get_user_view,
}
