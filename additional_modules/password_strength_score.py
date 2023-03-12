import math


def password_strength_chat_gpt(password):
    score = 0
    length = len(password)
    letters = set(password)
    digits = sum(c.isdigit() for c in password)
    upper_letters = sum(c.isupper() for c in password)
    lower_letters = sum(c.islower() for c in password)
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


def make_score_proportion(score):
    return int((score * 100) / 73)


def calculate_shannon_entropy(password):
    char_set = set(password)
    freq_list = [float(password.count(char)) / len(password) for char in char_set]
    entropy = -sum([freq * math.log(freq) / math.log(2.0) for freq in freq_list])
    return entropy


def password_strength(password):
    entropy = calculate_shannon_entropy(password)
    strength = min(int(entropy / 4 * 100), 100)
    return strength


def strength_rating(lange_state, password_score):
    if  0 <= password_score < 5:
        return 'Extremely unreliable' if lange_state else 'Мінімально надійний'
    elif 5 <= password_score < 20:
        return 'Very easy' if lange_state else 'Дуже простий'
    elif 20 <= password_score < 40:
        return 'Easy' if lange_state else 'Простий'
    elif 40 <= password_score < 60:
        return 'Below average' if lange_state else 'Нижче середнього'
    elif 60 <= password_score < 80:
        return 'Average' if lange_state else 'Середній'
    elif 80 <= password_score < 95:
        return 'Strong' if lange_state else 'Надійний'
    elif 95 <= password_score < 100:
        return 'Very strong' if lange_state else 'Дуже надійний'
    elif password_score == 100:
        return 'Extremely reliable' if lange_state else 'Максимально надійний'
