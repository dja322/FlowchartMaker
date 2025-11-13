import src.interface
import sys
    
def main() -> None:
    print("Initializing Interface")

    ROWHEIGHT = 1000
    COLHEIGHT = 1000

    if (len(sys.argv) == 2):
        try:
            ROWHEIGHT = int(sys.argv[1])
            COLHEIGHT = ROWHEIGHT
        except:
            print("Invalid Args, defaulting to 1000x1000 window")

    if (len(sys.argv) == 3):
        try:
            ROWHEIGHT = int(sys.argv[1])
            COLHEIGHT = int(sys.argv[2])
        except:
            print("Invalid Args, defaulting to 1000x1000 window")

    src.interface.cmdInterface(ROWHEIGHT, COLHEIGHT)

if __name__ == "__main__":
    main()