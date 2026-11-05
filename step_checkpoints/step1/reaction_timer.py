# Step 1: nickname
# Tested with: ab (too short), ab c (space), then Stitch1
# Result: the first two were refused; Stitch1 was accepted
from reaction_db import valid_player

player = input("Nickname (3 to 15 letters or digits): ").strip()
while not valid_player(player):
    print("Not valid. Use 3 to 15 letters or digits, no spaces.")
    player = input("Nickname (3 to 15 letters or digits): ").strip()
print(f"Welcome, {player}.")
