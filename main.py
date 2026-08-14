from quiz_data import get_questions
import random
import datetime

questions = get_questions()

print(questions)

random.shuffle(questions)
print("=" * 50)
# print(questions)

