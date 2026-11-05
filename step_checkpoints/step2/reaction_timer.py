# Step 2: five rounds saved to the database
# Tested with: one run with one wrong word, then a look at the row count
# Result: five rounds saved; the wrong word was repeated and not saved
from reaction_tools import play_round, show_early
from reaction_db import create_table, import_log, add_reaction, valid_player

ROUNDS = 5

create_table()
imported, damaged = import_log("typing_log.txt")
if imported > 0:
    print(f"Imported {imported} rounds from typing_log.txt as guest. ({damaged} damaged lines skipped)")

player = input("Nickname (3 to 15 letters or digits): ").strip()
while not valid_player(player):
    print("Not valid. Use 3 to 15 letters or digits, no spaces.")
    player = input("Nickname (3 to 15 letters or digits): ").strip()

print("Typing Sprint: when the green light comes on, type the word shown and press Enter.")
times = []
saved_count = 0
round_number = 1
while round_number <= ROUNDS:
    print(f"Round {round_number} of {ROUNDS}: wait for the green light.")
    seconds = play_round()
    if seconds is None:
        print("Not counted. The word must match exactly and take 5 seconds or less.")
        show_early()
    else:
        print(f"Typing time: {seconds:.3f} seconds")
        times.append(seconds)
        if add_reaction(seconds, player):
            saved_count = saved_count + 1
        round_number = round_number + 1

print(f"Saved {saved_count} of {ROUNDS} rounds.")
print(f"This run: average {sum(times) / len(times):.3f}, best {min(times):.3f}")
