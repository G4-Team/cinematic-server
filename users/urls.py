from users.views import get_user_view, is_auth_view, login_view, register_user_view

app_name = "users"

users_urls = {
    "get/{id}/": get_user_view,
    "login/": login_view,
    "register/": register_user_view,
    "is_auth/": is_auth_view,
}
