from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS
from annotator import Annotator
from answers import Answers
from analysis import Analysis

app = Flask(__name__)
CORS(app)

annotator = None
answer_catalog = None
analysis = None

@app.before_first_request
def initialize():
    global annotator, answer_catalog, analysis
    annotator = Annotator()
    answer_catalog = Answers()
    analysis = Analysis()


@app.route("/")
def index():
    global annotator, answer_catalog
    candidate = annotator.get_next_candidate()
    ranked_questions = annotator.get_similar_questions(candidate)
    answers = answer_catalog.answers
    return render_template("interface.html", name="Startpage", questions=ranked_questions, annotated_data=dict(), candidate=candidate, answers=answers)

@app.route("/candidate")
def candidate():
    global annotator, answer_catalog
    candidate = annotator.get_next_candidate()
    ranked_questions = annotator.get_similar_questions(candidate)
    answers = answer_catalog.answers

    # TODO: Remove improvised code
    for q in ranked_questions:
        q["preselect"] = False
    if len(ranked_questions) > 0:
        ranked_questions[0]["preselect"] = True

    return jsonify({
            "candidate": candidate,
            "ranked_questions": ranked_questions,
            "answers": answers
        })

@app.route("/getclusters")
def getclusters():
    clusters = analysis.get_clusters()
    # print(clusters)
    # return jsonify(clusters)
    return jsonify(
        clusters
    )


@app.route("/saveannotation", methods=["POST"])
def saveannotation():
    global annotator, answer_catalog
    try:
        """ Save Annotations to CSV File """
        label = request.form.get("labels", type=int)
        question_ids = request.form.getlist("questionlist[]", type=int)
        candidate_id = request.form.get("candidate", type=int)
        print(candidate_id)
        print(question_ids)
        print(label)
        if answer_catalog.check_valid_label(label):
            question_ids.append(candidate_id)
            annotator.save_annotations(label, question_ids)

            """ Remove Annotations from Questions Pool """
            annotator.remove_questions_from_pool(question_ids)

    except Exception as e:
        print("Something went wrong!")
        print(e)
    return candidate()


@app.route("/create_new_answer", methods=["POST"])
def create_new_answer():
    answer = request.form.get("answer", type=str)
    answer_short = request.form.get("answer-short", type=str)
    print(answer, answer_short)
    # TODO Create the new answer and return the ID
    aid = 123456
    return jsonify({
        "aid": aid
    })

@app.route("/get_overview", methods=["GET"])
# Input options for sort_by: "group" OR "label"
def get_overview():
    global annotator, answer_catalog
    sort_by = request.args.get('sort_by')
    annotated_groups = annotator.get_overview(sort_by, answer_catalog)
    return jsonify({
        "annotations": annotated_groups
    })

    # answer = request.form.get("answer", type=str)
    # answer_short = request.form.get("answer-short", type=str)
    # print(answer, answer_short)
    # # TODO Create the new answer and return the ID
    # aid = 123456
    # return jsonify({
    #     "aid": aid
    # })


@app.route("/reset", methods=["POST", "GET"])
def reset():
    global annotator, answer_catalog
    annotator = annotator.reset()
    answer_catalog = Answers()
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
