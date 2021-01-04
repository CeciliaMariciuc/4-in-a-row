import connect4
import sys


def get_level(computer):
    if "slab" in computer:
        return "slab"
    elif "mediu" in computer:
        return "mediu"
    else:
        return "avansat"


def main(argv):
    if len(argv) != 4:
        print("You need to enter 4 arguments!")
        sys.exit(0)
    rows = int(argv[1])
    cols = int(argv[2])
    first_player = argv[3]
    if argv[0] == "human":
        connect4.run_game_pvp(rows, cols, first_player)
    else:
        connect4.run_game_pvc(rows, cols, first_player, get_level(argv[0]))


if __name__ == '__main__':
    main(sys.argv[1:])
