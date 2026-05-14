from colorama import Fore, Style
from competence import competence_menu
from add import add_incidents_menu
from view import view_incidents
from delete import delete_incident_menu
from shared_functions import HomeException, BackException, clear_screen, get_input_with_navigation
from compare import compare_menu
from database import init_database


    #main menu loop.
def main():
    init_database()
    while True:
        try:
            #display menu
            clear_screen()
            print(Fore.WHITE+ "-----------------------------------------")
            print(Fore.YELLOW + "              Main Menu:" + Style.RESET_ALL)
            print("-----------------------------------------")
            print("1. Add new incident/s")
            print("2. View incident/s")
            print("3. Delete incident/s")
            print("4. Calculate for competence of month/s")
            print("5. Compare monthly scores")
            print(Fore.RED + "6. Exit" + Style.RESET_ALL)
            print("-----------------------------------------")

            #get choice
            choice = get_input_with_navigation("\nChoose an option (1-6): ").strip()

            #add incident
            if choice == "1":
                try:
                    add_incidents_menu()
                except HomeException:
                    continue

            #view incidents / search
            elif choice == "2":
                try:
                    view_incidents()
                except HomeException:
                    continue

            #delete incident
            elif choice == "3":
                try:
                    delete_incident_menu()
                except HomeException:
                    continue

            #calculate competence
            elif choice == "4":
                try:
                    competence_menu()
                except HomeException:
                    continue

            #compare scores
            elif choice == "5":
                try:
                    compare_menu()
                except HomeException:
                    continue
                
            #export to csv
            elif choice == "6":                
                try:
                    export_menu()
                except HomeException:
                    continue
        
            #exit program
            elif choice == "6":
                print("\nExiting....", 
                      "\nThank you for using this system, goodbye!")
                break 

            #invalid choice
            else:
                input("\nInvalid choice. Please choose (1-6).\n") 
        except (BackException, HomeException):
            # In main menu, BACK and HOME just continue the loop
            continue


if __name__ == "__main__":
    main() 