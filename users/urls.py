from users.views import (
    change_profile_view,
    login_view,
    profile_view,
    register_user_view,
)

app_name = "users"

users_urls = {
    "register/": register_user_view,
    "login/": login_view,
    "profile/{user_id}/": profile_view,
    "change-profile/{user_id}/": change_profile_view,
    "change-password/{user_id}/": None,
}
