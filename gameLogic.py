import Detect

# Assuming Detect module contains card detection logic
card_val = sum(Detect.cards)
dealer_val = sum(Detect.dealer)

# Also need a counter of aces for user

def logic():
    curr_ret = "S"  # Initial suggestion is to Stand
    
    if card_val == 21:
        return "S"
    
    # Hit logic
    if card_val == 8 or \
       (card_val == 9 and (dealer_val == 2 or dealer_val >= 7)) or \
       (card_val == 10 and (dealer_val >= 10)) or \
       (card_val == 12 and (dealer_val <= 3 or dealer_val >= 7)):
        return "H"
    
    # Double Down logic
    elif card_val == 11 or \
         (card_val == 10 and dealer_val <= 9) or \
         (card_val == 9 and dealer_val >= 3 and dealer_val <= 6):
        return "D"  # Suggest Double Down
    
    # Split logic
    elif card_val == 20:
        curr_ret = "P"  # Suggest Split
    
    # Surrender logic
    elif card_val == 15 and dealer_val == 10:
        curr_ret = "R"  # Suggest Surrender
    
    return curr_ret

# Example usage:
suggested_move = logic()
print(f"Suggested move: {suggested_move}")