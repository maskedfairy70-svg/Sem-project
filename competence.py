from shared_functions import score_calculation, clear_screen, prompt_try_another_month, validate_yes_no, BackException, HomeException, get_input_with_navigation, dates_of_incidents
from database import get_incidents_by_month, get_monthly_score, set_monthly_score, check_month_has_data, get_all_incidents
from colorama import Fore, Style

def competence_menu():
    while True:
        try:
            clear_screen()
            print("-----------------------------------")
            print(f"{Fore.YELLOW}        Calculate Score Menu:{Style.RESET_ALL}")
            print("-----------------------------------")
            print("1. Calculate for a single month")
            print("2. Calculate for all months")
            print("3. Return to main menu")
            print("-----------------------------------")
            print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
            choice = get_input_with_navigation("\nChoose an option (1-3): ").strip()

            if choice == "1":
                try:
                    calculate_single_month()
                except HomeException:
                    raise

            elif choice == "2":
                try:
                    calculate_all_months()
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

    #ask for a year/month, compute the overall score and replace or append it
def calculate_competence():
    while True:
        clear_screen()
            #ask for year and month
        dates_of_incidents()
        ym = get_input_with_navigation("\nEnter the date (YYYY-MM or type BACK/HOME): ").strip()

        try:
            year, month = map(int, ym.split("-"))
        except ValueError:
            input("Invalid format. Please use YYYY-MM format.")
            continue

            #check if month has data
        if not check_month_has_data(year, month):
            print(f"\nNo incidents found for {ym}.")
            if not prompt_try_another_month():
                return
            continue

            #get incidents
        incidents = get_incidents_by_month(year, month)

            #check if there's already a score
        existing_score = get_monthly_score(year, month)
        if existing_score is not None:
            print(f"\nThere's already a score for {ym}: {existing_score}")

            if not validate_yes_no("Do you want to recalculate the score? (y/n or type BACK/HOME): "):
                return

            #calculate score
        score = score_calculation(incidents)

        if score is None:
            print("Could not calculate score.")
            continue

            #save score to database
        try:
            set_monthly_score(year, month, score)
            print(f"\nScore for {ym} calculated and saved: {score}")
        except Exception as e:
            print(f"Error saving score: {e}")
            return

            #check other months?

        return
        
def calculate_single_month():
    while True:
        try:
            calculate_competence()
        except BackException:
            return
        except HomeException:
            raise

        try:
            if not validate_yes_no("\nCalculate for other months? (y/n or type BACK/HOME): "):
                return
        except BackException:
            return
        except HomeException:
            raise

def calculate_all_months():
    while True:
        try:
            clear_screen()
            incidents = get_all_incidents()
            incident_months = set()
            for incident in incidents:
                date_str = incident.get("Date and Time")
                if date_str:
                    try:
                        year, month = map(int, date_str.split("-")[:2])
                        incident_months.add((year, month))
                    except ValueError:
                        continue

            if not validate_yes_no("\nCalculate scores for all months without scores? (y/n or type BACK/HOME): "):
                return

            for year, month in incident_months:
                incidents = get_incidents_by_month(year, month)
                score = score_calculation(incidents)
                if score is not None:
                    set_monthly_score(year, month, score)
                    print(f"Calculated and saved score for {year}-{month:02d}: {score}")
                else:
                    print(f"Could not calculate score for {year}-{month:02d}.")

            if not validate_yes_no("\nAll done. Calculate again? (y/n or type BACK/HOME): "):
                return
        except BackException:
            return
        except HomeException:
            raise
