
from colorama import Fore, Style
from prettytable import PrettyTable
from shared_functions import HomeException, get_input_with_navigation, clear_screen, validate_yes_no, prompt_try_another_month, score_calculation, BackException
from database import get_incidents_by_month, get_monthly_score, check_month_has_data, get_all_monthly_scores

def compare_menu():
    while True:
        clear_screen()
        print("-----------------------------------")
        print(f"{Fore.YELLOW}     Compare Monthly Scores:{Style.RESET_ALL}")
        print("-----------------------------------")
        print("1. Compare two months")
        print("2. show all monthly scores")
        print("3. Return to main menu")
        print("-----------------------------------")
        print(f"(Type {Fore.CYAN}BACK{Style.RESET_ALL} to go back or {Fore.CYAN}HOME{Style.RESET_ALL} for main menu)")
        choice = get_input_with_navigation("\nChoose an option (1-3): ")

        if choice == "1":
            try:
                compare_scores()
            except HomeException:
                raise

        elif choice == "2":
            try:
                show_all_scores()
            except HomeException:
                raise
            
        elif choice == "3":
            return
        
        else:
            print("\nInvalid choice. Please choose 1 or 2.")
            input("Press Enter to continue...")

def show_all_scores():
    while True:
        clear_screen()
        print("-----------------------------------------")
        print(f"{Fore.YELLOW}Monthly Scores:{Style.RESET_ALL}")
        print("-----------------------------------------")
        scores = get_all_monthly_scores()
        if not scores:
            print("No monthly scores available.")
        else:
            table = PrettyTable()
            table.field_names = ["Year and Month", "Overall Score"]
            for score in scores:
                table.add_row([score["Year and Month"], score["Overall Score"]])
            print(table)
        print()

        try:
            if not get_input_with_navigation("Press Enter to reload or type BACK/HOME: "):
                continue
        except BackException:
            return
        except HomeException:
            raise

    
def compare_scores():
    clear_screen()
    #ask for two year/months, compute and print their scores and a simple comparison.#ask for two year/months, compute and print their scores and a simple comparison.
    while True:
            #ask for first year/month
        try:
            print("\nFor first month:", end="")
            ym1 = get_input_with_navigation("\nPlease enter year and month (YYYY-MM or type BACK/HOME): ").strip()
        except BackException:
            return
        except HomeException:
            raise

            #validate input format
        try:
            year1, month1 = map(int, ym1.split("-"))
        except ValueError:
            print("Invalid format. Please use YYYY-MM format.")
            continue

            #check if month has data
        if not check_month_has_data(year1, month1):
            print(f"\nNo incidents found for {ym1}.")
            if not prompt_try_another_month():
                return
            continue

            #get score from first month
        s1 = get_monthly_score(year1, month1)
        if s1 is None:
                #calculate score from incidents
            incidents1 = get_incidents_by_month(year1, month1)
            s1 = score_calculation(incidents1)

        if s1 is None:
            print("\nNo score available for first month.\n")
            return

            #ask for second year/month
        print("\nFor second month:", end="")
        try:
            ym2 = get_input_with_navigation("\nPlease enter year and month (YYYY-MM or type BACK/HOME): ").strip()
        except BackException:
            return
        except HomeException:
            raise
        try:
            year2, month2 = map(int, ym2.split("-"))
        except ValueError:
            print("Invalid format. Please use YYYY-MM format.")
            continue

            #check if month has data
        if not check_month_has_data(year2, month2):
            print(f"\nNo incidents found for {ym2}.")
            if not prompt_try_another_month():
                return
            continue

            #get score from second month
        s2 = get_monthly_score(year2, month2)
        if s2 is None:
                #calculate score from incidents
            incidents2 = get_incidents_by_month(year2, month2)
            s2 = score_calculation(incidents2)

        if s2 is None:
            print("\nNo score available for second month.\n")
            return

            #print result
        clear_screen()
        print(f"\nScore of {ym1}: {s1}")
        print(f"Score of {ym2}: {s2}\n")

            #month 1 is higher
        if s1 > s2:
            print(f"{ym1} scored higher than {ym2}.\n")

            #month 2 is higher
        elif s2 > s1:
            print(f"{ym2} scored higher than {ym1}.\n")

            #months are equal
        else:
            print("Both months have equal scores.\n")

        if not validate_yes_no("Compare other months? (y/n): "):
            return