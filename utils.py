# utils.py

import random
import string


def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32


def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))