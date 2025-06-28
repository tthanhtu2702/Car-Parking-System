"""Main Console for Car Parking Service."""
from ultils.colors import RED, RESET, GREEN, CYAN, BLUE, YELLOW
from handlers.parking_handler import handle_parking
from handlers.pickup_handler import handle_pickup
from handlers.history_handler import handle_history

def main():
    """Runs the main menu for the car parking system."""
    while True:
        try:
            print("=" * 20 + CYAN + " WELCOME TO THE CAR PARKING SYSTEM 🚗 " + RESET + "=" * 20)
            print("Please choose an option below:")
            print(YELLOW + "[1] Park A Car")
            print(YELLOW + "[2] Pick Up A Car")
            print(YELLOW + "[3] View Parking History")
            print(RESET + "[0] Exit The System")
            option = int(input(BLUE + "ENTER YOUR CHOICE (0–3): "))

            match option:
                case 0:
                    print(GREEN + "Thank you for using our service. See you next time!" + RESET)
                    break
                case 1:
                    handle_parking()
                case 2:
                    handle_pickup()
                case 3:
                    handle_history()
                case _:
                    print(RED + "Invalid option. Please select a number between 0 and 3." + RESET)

        except ValueError:
            print(RED + "Invalid input. Only numbers between 0 and 3 are accepted." + RESET)
        except KeyboardInterrupt:
            print(GREEN + "\nSession interrupted. Goodbye" + RESET)
            break

if __name__ == "__main__":
    main()
