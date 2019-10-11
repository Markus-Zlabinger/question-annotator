from flask import Flask, redirect, url_for, request, render_template
from annotator import Annotator
from answers import Answers

app = Flask(__name__)

ANN = None
ANS = None

@app.before_first_request
def initialize():
    global ANN, ANS
    ANN = Annotator()
    ANS = Answers()


@app.route("/")
def index():
    global ANN, ANS
    candidate = ANN.get_next_candidate()
    ranked_questions = ANN.get_similar_questions(candidate)
    answers = ANS.answers
    return render_template("interface.html", name="Startpage", questions=ranked_questions, annotated_data=dict(), candidate=candidate, answers=answers)


@app.route("/saveannotation", methods=["POST", "GET"])
def saveannotation():
    global ANN, ANS
    try:
        """ Save Annotations to CSV File """
        label = request.form.get("labels", type=str)
        if ANS.check_valid_label(label):
            question_ids = request.form.getlist("questionlist", type=int)
            candidate_id = request.form.get("candidate", type=int)
            question_ids.append(candidate_id)
            ANN.save_annotations(label, question_ids)

            """ Remove Annotations from Questions Pool """
            ANN.remove_questions_from_pool(question_ids)

    except Exception as e:
        print("Something went wrong!")
        print(e)
    return index()

@app.route("/reset", methods=["POST", "GET"])
def reset():
    global ANN, ANS
    ANN = ANN.reset()
    ANS = Answers()
    return index()



""" Methods """

""" Web Service Code """




# @app.route("/relabel", methods=["POST", "GET"])
# def relabel():
#     global QUESTION_POOL_ANNOT
#     global ANNOTATION_PATH
#     try:
#         newlabel = request.form.get("newlabel")
#         annotation_ids = request.form.getlist("annotationlist")
#         for qid_html in annotation_ids:
#             # print(qid_html)
#             # for Qestion-Id, label, text
#             for qid, question in QUESTION_POOL_ANNOT.items():
#                 # print(qid, qid_html, question)
#                 if qid_html == qid:
#                     # print("bin in if - Label ändern")
#                     # QUESTION_POOL_CSV[qid]=newlabel, tex
#                     QUESTION_POOL_ANNOT[qid] = newlabel, question[1]
#
#         # CSV Datei neu beschreiben:
#         s = csv.writer(open(ANNOTATION_PATH, "w", newline="", encoding="utf-8"), delimiter=",")
#         s.writerow(["Qestion ID", "Label", "Query"])
#         # print(QUESTION_POOL_ANNOT.items())
#         for qid, question in QUESTION_POOL_ANNOT.items():
#             # print(qid, question[0], question[1])
#             s.writerow([qid, question[0], question[1]])
#     except Exception as e:
#         print("Something went wrong!")
#         print(e)
#     return index()

if __name__ == "__main__":
    app.run()
