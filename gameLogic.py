# Game Logic Helper
def logic(player, dealer):

    ace_count = player.count('A') # Counter of aces for user
    # Removing ace card
    player = [card for card in player if card != 'A']

    card_val = sum(player)
    dealer_val = sum(dealer)

    curr_ret = "Stand"  # Initial suggestion is to Stand
    
    if card_val == 21:
        return "Stand"
    
    if card_val <= 7:
        return "Hit"
    
    # Hit logic
    if card_val == 8 or \
       (card_val == 9 and (dealer_val == 2 or dealer_val >= 7)) or \
       (card_val == 10 and (dealer_val >= 10)) or \
       (card_val == 12 and (dealer_val <= 3 or dealer_val >= 7)):
        return "Hit"
    
    # Double Down logic
    elif card_val == 11 or \
         (card_val == 10 and dealer_val <= 9) or \
         (card_val == 9 and dealer_val >= 3 and dealer_val <= 6):
        return "Double Down"  # Suggest Double Down
    
    # Split logic
    elif card_val == 20:
        curr_ret = "Split"  # Suggest Split
    
    # Surrender logic
    elif card_val == 15 and dealer_val == 10:
        curr_ret = "Surrender"  # Suggest Surrender
    
    return curr_ret
