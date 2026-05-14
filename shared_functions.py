from datetime import datetime
import math
import os

tru_dte = ""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def validate_yes_no(prompt):
    # validates y/n input and returns boolean
    while True:
        try:
            response = get_input_with_navigation(prompt).lower()
            if response == "y": 
                return True
            elif response == "n":
                return False
            else:
                print("Invalid input, please enter 'y' or 'n'.")
        except (BackException, HomeException):
            raise


def prompt_try_another_month():
    # prompts user if they want to try another month. Returns True to continue, False to exit
    return validate_yes_no("Try another month? (y/n or type BACK/HOME): ")


# format and validity test for date/time inputs, with confirmation

def format_test(dt_inc, guide):
    while True:
        # check for validity of the format
        bool_inc_dte, error_num = validity_test(dt_inc, guide)

        # if format is valid
        if bool_inc_dte == True and error_num == 0:
            break

        # if wrong format or date didn't exist
        elif bool_inc_dte == False and error_num == 1:
            dt_inc = get_input_with_navigation(f"Please ensure the format is ({guide}) and the date existed (or type BACK/HOME): ")

        # if date is in the future
        elif bool_inc_dte == False and error_num == 2:
            dt_inc = get_input_with_navigation(f"Please do not put future dates ({guide}) (or type BACK/HOME): ")

    # return the date
    return dt_inc


# validate date/time formats and check if not in the future

def validity_test(dt_inc, guide):
    try:
        # format for date
        if guide == "YYYY-MM-DD":
            # date to store
            dt_store = dt_inc

            # check if date or time follows format
            dt_inc = datetime.strptime(dt_inc, "%Y-%m-%d")

            # check if date hasn't happen yet
            if dt_inc > datetime.now():
                return False, 2

            # if the date is valid
            else:
                # record date for time check
                global tru_dte
                tru_dte = dt_store
                # return valid
                return True, 0

        # format for time
        elif guide == "HH:MM AM/PM":
            # check if date or time follows format
            datetime.strptime(dt_inc, "%I:%M %p")

            # get datetime
            dte_tim = (f"{tru_dte} {dt_inc}")

            # current time
            now = datetime.now()

            # check if time hasn't happen yet with date for 12 hr cycle
            dt_now = now.strftime("%Y-%m-%d %I:%M %p")
            if datetime.strptime(dte_tim, "%Y-%m-%d %I:%M %p") > datetime.strptime(dt_now, "%Y-%m-%d %I:%M %p"):
                return False, 2

            # if time is valid
            else:
                # return valid
                return True, 0

        # format for combined date and time
        elif guide == "YYYY-MM-DD HH:MM AM/PM":
            # check if follows format
            dt_parsed = datetime.strptime(dt_inc, "%Y-%m-%d %I:%M %p")

            # check if not in the future
            if dt_parsed > datetime.now():
                return False, 2

            # if valid
            else:
                return True, 0

    # if wrong format or date didn't exist
    except ValueError:
        return False, 1


# date/time and confirm the entered value

def date_time_check(guide):
    while True:
        # if date
        if guide == "YYYY-MM-DD":
            dt_type = "date"

        # if time
        elif guide == "HH:MM AM/PM":
            dt_type = "time"

        # if combined date and time
        elif guide == "YYYY-MM-DD HH:MM AM/PM":
            dt_type = "date and time"

        dt_inc = get_input_with_navigation(f"{dt_type} of the Incident ({guide}) (or type BACK/HOME): ")
        dt_inc = format_test(dt_inc, guide)

        # confirm
        while True:
            conf = get_input_with_navigation(f"The {dt_type} is {dt_inc}, confirm? (y/n or type BACK/HOME): ").lower()
            if conf == "y":
                return dt_inc
            elif conf == "n":
                break
            else:
                print("Invalid input, please try again!")
                continue


# score 0-5 for human or material damage, confirm, return score

def score_test(hum_or_mat, injury_or_damage):
    while True:
        # get score
        sco = get_input_with_navigation(f"\n{hum_or_mat} {injury_or_damage} severity (0-5 or type BACK/HOME): ")
        while True:
            # check if its a number
            if not sco.isdigit():
                sco = get_input_with_navigation("Please enter a whole number (or type BACK/HOME): ")
                continue

            # check if the month is valid
            sco_int = int(sco)
            if not (0 <= sco_int <= 5):
                sco = get_input_with_navigation("Please enter an integer from 0 to 5 (or type BACK/HOME): ")
                continue

            # confirm
            while True:
                conf = get_input_with_navigation(f"Is {sco_int} the right score? (y/n or type BACK/HOME): ").lower()
                if conf == "y":
                    return sco_int
                elif conf == "n":
                    break
                else:
                    print("Invalid input, please try again!")
                    continue
            break
        continue


# list of participants and confirm with the user

def confirm_participants(instruction):
    while True:
        # get participants
        print("")
        inc_typ = get_input_with_navigation(f"{instruction} (or type BACK/HOME): ")

        # confirm
        while True:
            conf = get_input_with_navigation(f"{inc_typ}. Is this all? (y/n or type BACK/HOME): ").lower()
            if conf == "n":
                break
            elif conf == "y":
                return inc_typ
            else:
                print("invalid input, try again!")
                continue
        continue

# print guide for scoring human/material damage severity
def parameters(dam, dam_mid, dam_max, percent, injury_or_damage):
    print(f"\nEnter an integer from 0 to 5 (this is {percent} of the overall score)")
    print(f"-- For {dam} {injury_or_damage}: 0 = {dam_max}, 2 = {dam_mid}, 5 = NONE. --")


# calculate average weighted score for a list of incident dicts.
def score_calculation(incidents):
    # list to put scores
    score = []

    # check each line
    for item in incidents:
        # skip per-item overall score entries and non-dict items
        try:
            if item.get("Overall Score: ") is not None:
                continue
        except AttributeError:
            # not dict-like, skip
            continue

        # store weighted score here
        inc_sco = 0

        # check each pair
        try:
            for key, value in item.items():
                # weighted damage score (combined human and material)
                if key == "Damage score":
                    # 100% weight and scale to 100
                    inc_sco += (int(value) * 1.0) * 20
        except AttributeError:
            # not dict-like, skip
            continue

        # append the weighted score to list
        score.append(inc_sco)

    # in case no incident records were found 
    if len(score) == 0:
        return 0

    # get the average
    average = math.fsum(score) / len(score)

    # return the rounded average
    return round(average)


class NavigationCommand(Exception):
    # base exception for navigation commands
    pass


class BackException(NavigationCommand):
    # exception to go back to the previous menu
    pass


class HomeException(NavigationCommand):
    # exception to go home to the main menu
    pass


def get_input_with_navigation(prompt):
    # get user input and handle BACK/HOME navigation commands
    user_input = input(prompt).strip().upper()

    if user_input == "BACK":
        raise BackException()
    elif user_input == "HOME":
        raise HomeException()

    return user_input.lower() if user_input in ["1", "2", "3", "4", "5"] else user_input
