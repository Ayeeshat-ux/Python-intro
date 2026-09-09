def calculate_average(scores):
    """Calculate and return the average of a list of scores."""
    return sum(scores) / len(scores)


def get_grade(average):
    """Return a letter grade based on the average score."""
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 60:
        return "C"
    else:
        return "F"


def generate_report(name, scores):
    """Print a student's name, average score, and letter grade."""
    average = calculate_average(scores)
    grade = get_grade(average)

    print(f"Student: {name}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")
    print("-" * 30)


generate_report("Aisha", [95, 88, 92, 90])
generate_report("David", [72, 68, 75, 70])
