from database import delete_incident_by_name, delete_all_incidents
from shared_functions import clear_screen, validate_yes_no, BackException, HomeException, get_input_with_navigation
from colorama import Fore, Style


def delete_incident_menu():
    while True:
        try:
            clear_screen()
            print("-----------------------------------")
            print(f"{Fore.YELLOW}       Delete Incident Menu:{Style.RESET_ALL}")
            print("-----------------------------------")
            print("1. Delete by incident name")
            print("2. Delete all incidents")
            print("3. Return to previous menu")
            print("-----------------------------------")
            print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            choice = get_input_with_navigation("\nChoose an option (1-3): ")

            if choice == "1":
                try:
                    delete_by_name()
                except BackException:
                    continue
                except HomeException:
                    raise
            elif choice == "2":
                try:
                    delete_all()
                except BackException:
                    continue
                except HomeException:
                    raise
            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please choose 1, 2, or 3.")
                input("Press Enter to continue...")
        except BackException:
            return
        except HomeException:
            raise


def delete_by_name():
    while True:
        try:
            clear_screen()
            inc_name = get_input_with_navigation("\nEnter the incident name to delete (or type BACK/HOME): ")
            if not inc_name:
                print("Incident name cannot be empty.")
                continue

            if validate_yes_no(f"Are you sure you want to delete '{inc_name}'? (y/n or type BACK/HOME): "):
                if delete_incident_by_name(inc_name):
                    print(f"\nIncident '{inc_name}' deleted successfully.")
                else:
                    print(f"\nNo incident found with name '{inc_name}'.")

            if not validate_yes_no("\nDelete another incident? (y/n or type BACK/HOME): "):
                return
        except BackException:
            return
        except HomeException:
            raise


def delete_all():
    while True:
        clear_screen()
        try:
            user_input = get_input_with_navigation("Are you sure you want to delete ALL incidents? (y/n or type BACK/HOME): ").lower()
            if user_input in ["y", "yes"]:
                delete_all_incidents()
                print("\nAll incidents have been deleted.")
                break
            elif user_input in ["n", "no"]:
                print("\nDeletion cancelled.")
                break
            else:
                print("\nPlease enter 'y' or 'n'.")
                input("Press Enter to continue...")
        except BackException:
            return
        except HomeException:
            raise

    input("\nPress Enter to continue...")
