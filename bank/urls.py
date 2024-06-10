from bank.views import add_card_view, deposit_view, list_cards_view

app_name = "bank"

bank_urls = {
    "card/add/{user_id}/": add_card_view,
    "card/list/{user_id}/": list_cards_view,
    "card/deposit/{user_id}/{card_id}/": deposit_view,
    "card/withdrawal/{user_id}/{card_id}/": None,
    "card/wire-transfer/{user_id}/{card_id}/": None,
}
