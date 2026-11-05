# Step 4: leaderboard
# Tested with: two nicknames, then a third run
# Result: the board listed each nickname once with its best time and number of rounds
from reaction_tools import play_round, show_early, show_best
from reaction_db import create_table, import_log, add_reaction, valid_player, player_summary, leaderboard

ROUNDS = 5

create_table()
imported, damaged = import_log("typing_log.txt")
if imported > 0:
    print(f"Imported {imported} rounds from typing_log.txt as guest. ({damaged} damaged lines skipped)")

player = input("Nickname (3 to 15 letters or digits): ").strip()
while not valid_player(player):
    print("Not valid. Use 3 to 15 letters or digits, no spaces.")
    player = input("Nickname (3 to 15 letters or digits): ").strip()

earlier = player_summary(player)
if earlier is None:
    print(f"Welcome, {player}. No saved rounds yet.")
else:
    print(f"Welcome back, {player}. Saved rounds: {earlier[0]}, best {earlier[1]:.3f} seconds.")

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

if earlier is not None and min(times) < earlier[1]:
    print("New personal best!")
    show_best()

print("Leaderboard:")
for place, row in enumerate(leaderboard(3), start=1):
    print(f"  {place}. {row[0]:<15}{row[1]:.3f} seconds  ({row[2]} rounds)")
