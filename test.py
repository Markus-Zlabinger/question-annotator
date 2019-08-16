import config
import csv

savepath="annot.csv"
questions = dict()
qidx = 0
with open(config.PATH_QUESTIONS, mode="r", encoding="utf-8") as f:
    for index, line in enumerate(f):
        question_text = line.strip()
        if question_text:  # Ignore empty lines
            questions[str(qidx)] = question_text
            qidx += 1

# for qid, quest in questions.items():
#    print(qid,quest)
# for qid in questions:
#     print(qid,questions[qid])

# with open(savepath, mode="a", encoding="utf-8") as s:
s = csv.writer(open(savepath, "w", newline='', encoding="utf-8"), delimiter=",")
s.writerow(["Hans","Franz"])
for qid, ling in questions.items():
    tex = ling.strip()
    s.writerow([qid,tex])
