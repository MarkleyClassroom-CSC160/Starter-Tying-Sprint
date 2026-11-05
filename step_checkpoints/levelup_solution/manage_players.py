# Step 5: manage_players.py
# Tested with: renaming guest, then deleting a test nickname
# Result: guest became my nickname; the delete asked for YES and reported the rows removed
from reaction_db import valid_player, player_summary, rename_player, delete_player

choice = input("[r]ename a nickname, [d]elete a nickname, [q]uit: ").strip().lower()
while choice != "q":
    if choice == "r":
        old = input("Rename which nickname? ").strip()
        new = input("New nickname: ").strip()
        if not valid_player(new):
            print("Not valid. Nothing changed.")
        else:
            print(f"Changed {rename_player(old, new)} rounds.")
    elif choice == "d":
        old = input("Delete which nickname? ").strip()
        found = player_summary(old)
        if found is None:
            print("No rounds for that nickname.")
        else:
            answer = input(f"This removes {found[0]} rounds. Type YES to continue: ")
            if answer == "YES":
                print(f"Deleted {delete_player(old)} rounds.")
            else:
                print("Nothing deleted.")
    else:
        print("Choose r, d, or q.")
    choice = input("[r]ename a nickname, [d]elete a nickname, [q]uit: ").strip().lower()
