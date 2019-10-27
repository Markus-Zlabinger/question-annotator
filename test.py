import numpy
import config

print("lol")

with open(config.PATH_QUESTIONS, mode="r", encoding="utf-8") as f:
    for index, line in enumerate(f):
        question_text = line.strip()
        if question_text:
            questions.append(question_text)

for i, q in enumerate(questions):
    print("{},{}".format(i, q))