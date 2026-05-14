# export data from database to csv file
import csv
from database import get_all_incidents
from shared_functions import available_incidents, clear_screen, get_input_with_navigation, BackException, HomeException, validate_yes_no
from colorama import Fore, Style
import os


def export_menu():
    while True:
        try:
            clear_screen()
            print("-----------------------------------")
            print(f"{Fore.YELLOW}       Export Incidents to CSV:{Style.RESET_ALL}")
            print("-----------------------------------")
            print("1. Export incident/s to CSV")
            print("2. Export all incidents to CSV")
            print("3. Return to main menu")
            print("-----------------------------------")
            print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            choice = get_input_with_navigation("\nEnter your choice: ")

            if choice == "1":
                export_to_csv()

            elif choice == "2":
                export_all_to_csv()

            elif choice == "3":
                return
            
            else:
                input("Invalid choice. Please try again.")
        except BackException:
            return
        except HomeException:
            raise

def export_to_csv():
    while True:
        try:
            clear_screen()
            filename = get_input_with_navigation("Enter the filename to export (or type BACK/HOME): ").strip()
            if not filename:
                print("Filename cannot be empty.")
                continue

            filename += ".csv"
            incidents = get_all_incidents()

            while True:
                clear_screen()
                available_incidents()
                file_exists = os.path.isfile(filename)

                incident_names_to_export = get_input_with_navigation("\nEnter the incident name to export (or type BACK/HOME): ").strip()

                if incident_names_to_export not in [incident['Incident name'] for incident in incidents]:
                    print("Incident not found.")

                    if not validate_yes_no("\nAdd another incident to export? (y/n or type BACK/HOME): "):
                        break

                with open(filename, 'a', newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=incidents[0].keys())

                    if not file_exists:
                        writer.writeheader()

                    writer.writerows(incident for incident in incidents if incident['Incident name'] == incident_names_to_export)

                print(f"\nIncident successfully exported to {filename}.")
                if not validate_yes_no("\nAdd another incident to export? (y/n or type BACK/HOME): "):
                    break
            return

        except BackException:
            return
        except HomeException:
            raise

def export_all_to_csv():
    while True:
        try:
            clear_screen()
            filename = get_input_with_navigation("Enter the filename to export all incidents (or type BACK/HOME): ").strip()
            if not filename:
                print("Filename cannot be empty.")
                continue

            filename += ".csv"
            incidents = get_all_incidents()

            if not incidents:
                print("No incidents to export.")
                input("Press Enter to continue...")
                if not validate_yes_no("\nTry again? (y/n or type BACK/HOME): "):
                    return
                else:
                    continue

            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=incidents[0].keys())
                writer.writeheader()
                writer.writerows(incidents)

            print(f"\nAll incidents successfully exported to {filename}.")
            if not validate_yes_no("\nExport another file? (y/n or type BACK/HOME): "):
                return
        except BackException:
            return
        except HomeException:
            raise