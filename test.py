import config
import csv

savepath="annot.csv"
# ************* aus Text File daten auslesen: ****************
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

#*********** Einzelne daten auslesen ********************
# zuerst oben qustions laden ausführen!!!!!!!
vorhanden=list()
with open(savepath, mode="r", encoding="utf-8") as f:
    s=csv.reader(f, delimiter=",")
    # print(list(s)[0][2])
    # for label, idn, querry in s:
    for idn in s:
        # print(idn[1], idn[2])
        for num, line in questions.items():
            if num == idn[1] and line == idn[2]:
                print("schon enthalten: %s", num, line)
                vorhanden.append(num)
print("bereits annotiert: ", vorhanden)
#remove_questions_from_pool(set(vorhanden))

#funkt:
# vorhanden=dict()
# qidx2 = 0
# with open(savepath, mode="r", encoding="utf-8") as f:
#     s=csv.reader(f, delimiter=",")
#     # print(list(s)[0][2])
#     for label, idn, querry in s:
#         # print(label,querry)
#         for num, line in questions.items():
#             if num==idn:
#                 # print("schon enthalten: %s", line)
#                 vorhanden[str(qidx2)]=([label, idn, line])
#                 qidx2+=1
# print(vorhanden)

