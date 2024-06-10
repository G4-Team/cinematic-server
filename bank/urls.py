from bank.views import (
    add_card_view,
    deposit_view,
    list_cards_view,
    wire_transfer_view,
    withdrawal_view,
)

app_name = "bank"

bank_urls = {
    "card/add/{user_id}/": add_card_view,
    "card/list/{user_id}/": list_cards_view,
    "card/deposit/{user_id}/{card_id}/": deposit_view,
    "card/withdrawal/{user_id}/{card_id}/": withdrawal_view,
    "card/wire-transfer/{user_id}/{sending_card_id}/": wire_transfer_view,
}
