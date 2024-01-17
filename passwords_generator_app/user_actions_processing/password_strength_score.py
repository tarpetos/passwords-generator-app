import math

from passwords_generator_app.app_translation.load_data_for_localization import (
    LOCALIZATION_DATA,
)


def password_strength_chat_gpt(password: str) -> int:
    score = 0
    length = len(password)
    letters = set(password)
    digits = sum(char.isdigit() for char in password)
    upper_letters = sum(char.isupper() for char in password)
    lower_letters = sum(char.islower() for char in password)
    symbols = length - digits - upper_letters - lower_letters

    score += min(10, length)

    if digits:
        score += min(10, digits * 4)

    if upper_letters and lower_letters:
        score += min(20, (upper_letters + lower_letters) * 2)

    if symbols:
        score += min(25, symbols * 6)

    if letters:
        score += min(5, len(letters))

    if digits and letters and symbols:
        score += min(5, 3)

    return score


def make_score_proportion(score: int) -> int:
    return int((score * 100) / 73)


def calculate_shannon_entropy(password: str) -> float:
    char_set = set(password)
    freq_list = [float(password.count(char)) / len(password) for char in char_set]
    entropy = -sum([freq * math.log(freq) / math.log(2.0) for freq in freq_list])
    return entropy


def password_strength(password: str) -> int:
    entropy = calculate_shannon_entropy(password)
    strength = min(int(entropy / 4 * 100), 100)
    return strength


def strength_rating(lang_state: str, password_score: int) -> str:
    password_score_options = {
        range(0, 5): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][0],
        range(5, 20): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][1],
        range(20, 40): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][2],
        range(40, 60): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][3],
        range(60, 80): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][4],
        range(80, 95): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][5],
        range(95, 100): LOCALIZATION_DATA[lang_state]["symbols_option_menu"][6],
        100: LOCALIZATION_DATA[lang_state]["symbols_option_menu"][7],
    }

    for key in password_score_options:
        if (isinstance(key, int) and key == password_score) or (
            isinstance(key, range) and password_score in key
        ):
            return password_score_options[key]
