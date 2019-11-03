from flask import Flask, redirect, url_for, request, render_template, jsonify, abort
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
def candidate(cluster_preselect=True):
    global annotator, answer_catalog
    current_candidate = annotator.get_next_candidate()
    ranked_questions = list()
    if current_candidate:
        preselect_ids = set()
        if cluster_preselect:
            preselect_ids = analysis.get_preselect(current_candidate["qid"])
        ranked_questions = annotator.get_similar_questions(current_candidate, preselect_ids=preselect_ids)
    answers = answer_catalog.answers

    return jsonify({
        "candidate": current_candidate,
        "ranked_questions": ranked_questions,
        "answers": answers
    })

@app.route("/getanswers", methods=["POST"])
def getanswers():
    global answer_catalog
    qids = request.form.getlist("qids[]", type=str)
    print(qids)
    return jsonify({
        "answers": answer_catalog.get_ranked_answers(qids)
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
        labels = request.form.getlist("labels[]", type=str)
        question_ids = request.form.getlist("questionlist[]", type=str)
        # candidate_id = request.form.get("candidate", type=int)
        # print(candidate_id)
        print(question_ids)
        print(labels)
        # question_ids.append(candidate_id)
        if len(labels) == 0:
            abort()
        for label in labels:
            annotator.save_annotations(label, question_ids)

        """ Remove Annotations from Questions Pool """
        annotator.remove_questions_from_pool(question_ids)

    except Exception as e:
        print("Something went wrong!")
        print(e)
        abort()
    return ""


@app.route("/modifyannotation", methods=["POST"])
def modifyannotation():
    global annotator, answer_catalog
    qid = request.form.get("qid", type=str)
    answerlabels = request.form.getlist("labels[]", type=str)
    annotator.modify_annotation(qid, answerlabels)
    return ""


# @app.route("/create_new_answer", methods=["POST"])
# def create_new_answer():
#     global answer_catalog
#     answer = request.form.get("answer", type=str)
#     answer_short = request.form.get("answer-short", type=str)
#     print(answer, answer_short)
#     answer_catalog.add_answer(answer, answer_short)
#     # TODO Create the new answer and return the ID
#     aid = 123456
#     return jsonify({
#         "aid": aid
#     })

@app.route("/deleteannotation", methods=["POST"])
def delete_annotation():
    qid = request.form.getlist("qid", type=str)
    aid = request.form.getlist("aid", type=str)
    print(qid, aid)


@app.route("/get_overview", methods=["GET"])
# Input options for sort_by: "group" OR "label"
def get_overview():
    global annotator, answer_catalog
    sort_by = request.args.get('sort_by')
    annotated_groups = annotator.get_overview(sort_by, answer_catalog)
    return jsonify({
        "annotations": annotated_groups,
        "answer_dict": {a["aid"]: a for a in answer_catalog.answers},
        # "answers": answer_catalog.answers,
        # "answer_ids": answer_catalog.answer_ids,
        "questions": annotator.questions,
        "question_ids": annotator.question_ids
    })


# @app.route("/getanswers", methods=["GET"])
# def getanswers():
#     global answer_catalog
#     return jsonify({
#         "answers": answer_catalog.answers,
#     })


@app.route("/reset", methods=["GET"])
def reset():
    global annotator, answer_catalog
    annotator = annotator.reset()
    answer_catalog = Answers()
    # return index()
    return ""


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
