from bank.views import add_card_view

app_name = "bank"

bank_urls = {
    "card/add/{user_id}/": add_card_view,
    "card/list/{user_id}": None,
}
