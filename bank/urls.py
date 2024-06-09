from bank.views import add_card_view, list_cards_view

app_name = "bank"

bank_urls = {
    "card/add/{user_id}/": add_card_view,
    "card/list/{user_id}/": list_cards_view,
}
