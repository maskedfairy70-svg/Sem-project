from prettytable import PrettyTable, ALL
from database import get_all_incidents, get_incident_by_name
from shared_functions import available_incidents, clear_screen, validate_yes_no, BackException, HomeException, get_input_with_navigation
from colorama import Fore, Style


def render_incidents(incidents, title):
    clear_screen()
    single_search = len(incidents) == 1 and title.startswith("Incident:")

    if single_search:
        print("-----------------------------------",
              f"\n{title}",
              "\n-----------------------------------")
    else:
        print("-----------------------------------",
              f"\n{title}",
              "\n-----------------------------------",
              "\nIncidents:",
              "\n-----------------------------------")

    if not incidents:
        print("No incidents to display.")
    else:
        if len(incidents) == 1 and single_search:
            # for a single searched incident, show only the table
            incident = incidents[0]
            table = PrettyTable()
            table.field_names = [
                f"{Fore.YELLOW}Info{Style.RESET_ALL}",
                f"{Fore.YELLOW}Details{Style.RESET_ALL}"
            ]
            table.hrules = ALL

            for key, value in incident.items():
                table.add_row([key, value])

            print(table)
        elif len(incidents) == 1:
            # for single incident from the full list, show a vertical table
            for i, incident in enumerate(incidents, start=1):
                table = PrettyTable()
                table.field_names = [
                    f"{Fore.YELLOW}Info{Style.RESET_ALL}",
                    f"{Fore.YELLOW}Details{Style.RESET_ALL}"
                ]
                table.hrules = ALL

                for key, value in incident.items():
                    table.add_row([key, value])

                print(f"\nINCIDENT #{i}")
                print(table)
        else:
            # for multiple incidents, show a horizontal table
            table = PrettyTable()
            if incidents:
                # get field names from first incident (colored headers)
                field_names = [f"{Fore.YELLOW}{key}{Style.RESET_ALL}" for key in incidents[0].keys()]
                table.field_names = field_names
                table.hrules = ALL

                # Add each incident as a row
                for incident in incidents:
                    table.add_row([str(value) for value in incident.values()])

            print(table)


def view_all_incidents():
    while True:
        try:
            incidents = get_all_incidents()
            render_incidents(incidents, "All Recorded Incidents")
            print(f"\n(Type {Fore.CYAN}BACK{Style.RESET_ALL} to return to View menu or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            if not get_input_with_navigation("\nPress Enter to reload, or type BACK/HOME: ").strip().upper() == "BACK":
                continue
        except BackException:
            return
        except HomeException:
            raise

def view_incidents():
    while True:
        try:
            clear_screen()
            print("-----------------------------------")
            print(f"{Fore.YELLOW}       View Incidents Menu:{Style.RESET_ALL}")
            print("-----------------------------------")
            print("1. View all incidents")
            print("2. Search incident")
            print("3. Return to main menu")
            print("-----------------------------------")
            print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            choice = get_input_with_navigation("\nChoose an option (1-3): ")

            if choice == "1":
                view_all_incidents()

            elif choice == "2":
                search_incident()

            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please choose 1, 2, or 3.")
                input("Press Enter to continue...")
        except BackException:
            return
        except HomeException:
            raise


def search_incident():
    while True:
        clear_screen()
        try:
            available_incidents()
            #ask for incident name
            inc_name = get_input_with_navigation("\nPlease enter the incident name (or type BACK/HOME): ")

            if not inc_name:
                print("Incident name cannot be empty.")
                continue

            #get incident from database
            incident = get_incident_by_name(inc_name)

            if not incident:
                print(f"\nNo incident found with name '{inc_name}'.")
                if not validate_yes_no("\nTry searching for another incident? (y/n or type BACK/HOME): "):
                    return
                continue
            
            #display the incident
            render_incidents([incident], f"Incident: {inc_name}")

            #check if want to search other incidents
            if not validate_yes_no("\nSearch for another incident? (y/n or type BACK/HOME): "):
                return
        except BackException:
            return
        except HomeException:
            raise