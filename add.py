from shared_functions import date_time_check, confirm_participants, parameters, score_test, clear_screen, BackException, HomeException, get_input_with_navigation
from database import add_incident_to_db
from datetime import datetime
from colorama import Fore, Style


def add_incidents_menu():
    while True:
        try:
            clear_screen()
            print("-----------------------------------")
            print(f"{Fore.YELLOW}     Add Incidents Menu:{Style.RESET_ALL}")
            print("-----------------------------------")
            print("1. Add incident")
            print("2. Add multiple incidents")
            print("3. Return to main menu")
            print("-----------------------------------")
            print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            choice = get_input_with_navigation("\nChoose an option (1-3): ")

            if choice == "1":
                try:
                    add_single_incident()
                except HomeException:
                    raise

            elif choice == "2":
                try:
                    add_multiple_incidents()
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


    #input data and append it to database (single incident)
def add_single_incident():
    while True:
        try:
            #get dictionary from input function
            data = input_incident()
        except BackException:
            return
        except HomeException:
            raise

            #add incident to database
        try:
            add_incident_to_db(data)
            print("Incident added successfully!")
        except Exception as e:
            print(f"Error adding incident: {e}")
            return

        try:
            while True:
                result = get_input_with_navigation("\nAdd another? (y/n or type BACK/HOME): ").lower()
                if result == "y":
                    break
                elif result == "n":
                    return
                else:
                    print("Invalid input, please try again!")
                    continue
        except BackException:
            return  # Treat BACK as "no"
        except HomeException:
            raise


def add_multiple_incidents():
    while True:
        try:
            #get dictionary from input function
            data = input_incident()
        except BackException:
            return
        except HomeException:
            raise

            #add incident to database
        try:
            add_incident_to_db(data)
            print("\nIncident added successfully!")
        except Exception as e:
            print(f"Error adding incident: {e}")
            return

        # Automatically continue to add another incident
        input("\nReady to add another incident...")
        

    #inputs to build an incident dict
def input_incident():
        #incident name
    clear_screen()
    inc_nam = get_input_with_navigation("Incident name (or type BACK/HOME): ").strip()
    while not inc_nam:
        print("Incident name cannot be empty.")
        inc_nam = get_input_with_navigation("Incident name (or type BACK/HOME): ").strip()

        #date and time combined
    clear_screen()
    tru_dt = date_time_check("YYYY-MM-DD HH:MM AM/PM")

        #incident type
    clear_screen()
    inc_typ = confirm_participants("Incident Details")

        #persons involved and guards on duty combined
    clear_screen()
    per_grd = confirm_participants("People involved")

        #combined damage score (human and material)
    clear_screen()
    parameters("overall", "will leave a permanent mark or not recoverable", "fatal or fatally hazardous", "50%", "damage")

        #overall damage score
    dmg_sco = score_test("overall", "damage")

        #record current date/time
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %I:%M %p")

        #dictionary to contain details
    incident = {
        "Incident name": inc_nam,
        "Incident Details": inc_typ,
        "Date and Time": tru_dt,
        "People involved": per_grd,
        "Damage score": dmg_sco,
        "Incident recorded at": now
    }
    return incident