from users.views import (
    buy_subscription_view,
    change_password_view,
    change_profile_view,
    charge_wallet_view,
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
    "change-password/{user_id}/": change_password_view,
    "charge-wallet/{user_id}/": charge_wallet_view,
    "buy-subscription/{user_id}/": buy_subscription_view,
}
