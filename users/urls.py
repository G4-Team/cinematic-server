from users.views import is_auth_view, login_view, profile_view, register_user_view

app_name = "users"

users_urls = {
    "register/": register_user_view,
    "login/": login_view,
    "profile/{user_id}/": profile_view,
    "is_auth/": is_auth_view,
}
