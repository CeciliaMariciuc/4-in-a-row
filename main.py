import connect4
import sys


def get_level(computer):
    """
    Returneaza nivelul de dificultate, in functie de tipul computerului
    """
    if "slab" in computer:
        return "slab"
    elif "mediu" in computer:
        return "mediu"
    else:
        return "avansat"


def main(argv):
    """
        Rularea tipului de joc dorit.
        - argument 1: tipul de player (valori: human, computer_avansat, computer_mediu, computer_slab)
        - argument 2: numar linii
        - argument 3: numar coloane
        - argument 4: primul jucator(valori pt joc versus human: human1, human2)
                                    (valori pt joc versus computer: human, computer)
    """
    if len(argv) != 4:
        print("You need to enter 4 arguments!")
        sys.exit(0)
    rows = int(argv[1])
    cols = int(argv[2])
    if rows < 4 or cols < 4:
        print("The board needs at least 4 rows and 4 columns!")
        sys.exit(0)
    first_player = argv[3]
    if argv[0] == "human":
        connect4.run_game_pvp(rows, cols, first_player)
    else:
        connect4.run_game_pvc(rows, cols, first_player, get_level(argv[0]))


if __name__ == '__main__':
    main(sys.argv[1:])
