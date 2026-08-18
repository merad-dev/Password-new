#!/usr/bin/env python3
import secrets
import string
import sys
import os


if os.name == 'nt':
    os.system('')

class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    ascii_art = r"""
  ____                                     _ 
 |  _ \ __ _ ___ _____      _____  _ __ __| |
 | |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |
 |  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |
 |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
"""
    print(f"{C.CYAN}{C.BOLD}{ascii_art}{C.RESET}")
    print(f"{C.YELLOW}{C.BOLD}     PASSWORD GENERATOR TOOL{C.RESET}")
    print(f"{C.MAGENTA}     Telegram: {C.BOLD}@MeradDev_Official{C.RESET}")

def print_box(text, color=C.GREEN):
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 4
    border = '+' + '-' * (width - 2) + '+'
    print(f"{color}{border}{C.RESET}")
    for line in lines:
        print(f"{color}| {line.ljust(width - 4)} |{C.RESET}")
    print(f"{color}{border}{C.RESET}")

def get_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    if length < 1:
        return "Error: length must be at least 1."
    if length < 4 and sum([use_upper, use_lower, use_digits, use_symbols]) > length:
        return "Error: length too short for selected character types."

    pools = []
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    if not pools:
        return "Error: select at least one character type."

    # ضمان وجود حرف واحد على الأقل من كل نوع مختار
    password_chars = [secrets.choice(pool) for pool in pools]
    all_chars = ''.join(pools)
    remaining = length - len(password_chars)

    if remaining > 0:
        password_chars.extend(secrets.choice(all_chars) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def password_strength(password, upper, lower, digits, symbols):
    score = 0
    if upper: score += 1
    if lower: score += 1
    if digits: score += 1
    if symbols: score += 1

    length = len(password)
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if length >= 20: score += 1

    if score <= 2:
        return "Weak", C.RED
    elif score <= 4:
        return "Medium", C.YELLOW
    elif score <= 6:
        return "Strong", C.GREEN
    else:
        return "Very Strong", C.CYAN

def prompt_int(prompt, default):
    try:
        val = input(f"{C.CYAN}{prompt} [{default}]: {C.RESET}").strip()
        if val == '':
            return default
        return int(val)
    except ValueError:
        return default

def prompt_yes_no(prompt, default=True):
    suffix = "(Y/n)" if default else "(y/N)"
    val = input(f"{C.CYAN}{prompt} {suffix}: {C.RESET}").strip().lower()
    if val == '':
        return default
    return val in ('y', 'yes', '1', 'true')

def customize(settings):
    print_box("CUSTOMIZE PASSWORD SETTINGS", C.YELLOW)

    settings['length'] = prompt_int("Password length", settings['length'])
    if settings['length'] < 4:
        print(f"{C.RED}Warning: length < 4 may cause issues with multiple character types.{C.RESET}")

    settings['upper'] = prompt_yes_no("Include uppercase letters (A-Z)", settings['upper'])
    settings['lower'] = prompt_yes_no("Include lowercase letters (a-z)", settings['lower'])
    settings['digits'] = prompt_yes_no("Include digits (0-9)", settings['digits'])
    settings['symbols'] = prompt_yes_no("Include special/twisted symbols (!@#$...)", settings['symbols'])

    if not any([settings['upper'], settings['lower'], settings['digits'], settings['symbols']]):
        print(f"{C.RED}You must select at least one character type!{C.RESET}")
        settings['lower'] = True

    print_box("Settings saved!", C.GREEN)
    return settings

def show_settings(settings):
    text = (
        f"Length: {settings['length']}\n"
        f"Uppercase: {settings['upper']}\n"
        f"Lowercase: {settings['lower']}\n"
        f"Digits: {settings['digits']}\n"
        f"Symbols: {settings['symbols']}"
    )
    print_box(text, C.BLUE)

def main():
    clear_screen()
    banner()

    settings = {
        'length': 16,
        'upper': True,
        'lower': True,
        'digits': True,
        'symbols': True,
    }

    # توليد كلمة سر افتراضية تلقائيًا
    print_box("DEFAULT PASSWORD", C.MAGENTA)
    pwd = get_password(
        settings['length'],
        settings['upper'],
        settings['lower'],
        settings['digits'],
        settings['symbols']
    )
    if pwd.startswith('Error'):
        print(f"{C.RED}{C.BOLD}{pwd}{C.RESET}\n")
    else:
        print(f"{C.BOLD}{C.GREEN}{pwd}{C.RESET}")
        label, color = password_strength(
            pwd,
            settings['upper'],
            settings['lower'],
            settings['digits'],
            settings['symbols']
        )
        print(f"{color}Strength: {label}{C.RESET}\n")

    while True:
        print(f"{C.YELLOW}{C.BOLD}MENU:{C.RESET}")
        print(f"  {C.CYAN}1{C.RESET}. Generate new password")
        print(f"  {C.CYAN}2{C.RESET}. Customize settings")
        print(f"  {C.CYAN}3{C.RESET}. Show current settings")
        print(f"  {C.CYAN}4{C.RESET}. Exit")

        choice = input(f"{C.BOLD}{C.GREEN}>> {C.RESET}").strip()

        if choice == '1':
            pwd = get_password(
                settings['length'],
                settings['upper'],
                settings['lower'],
                settings['digits'],
                settings['symbols']
            )
            print_box("YOUR NEW PASSWORD", C.GREEN)
            if pwd.startswith('Error'):
                print(f"{C.RED}{C.BOLD}{pwd}{C.RESET}\n")
            else:
                print(f"{C.BOLD}{C.GREEN}{pwd}{C.RESET}")
                label, color = password_strength(
                    pwd,
                    settings['upper'],
                    settings['lower'],
                    settings['digits'],
                    settings['symbols']
                )
                print(f"{color}Strength: {label}{C.RESET}\n")

        elif choice == '2':
            settings = customize(settings)

        elif choice == '3':
            show_settings(settings)

        elif choice == '4':
            print(f"{C.RED}{C.BOLD}Goodbye!{C.RESET}")
            sys.exit(0)

        else:
            print(f"{C.RED}Invalid option. Try again.{C.RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}Exiting...{C.RESET}")
        sys.exit(0)
