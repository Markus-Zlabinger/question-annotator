import defaultsettings
from flask import Flask, redirect, url_for, request, render_template
from src.data_io import load_questions, load_annotations
import csv
import config
import random
import os
import numpy as np
#
# app.debug = True
import pickle

app = Flask(__name__)

# Load Global Variables
QUESTION_POOL = None
QUESTION_POOL_ANNOT = None
SIM_MATRIX = None
CSVpath = "./annotations/annotations.csv"

""" Methods """


# Returns a list of similar questions (neighbors) with respect to a query question
def get_ranked_neighbors(rowidx):
    global SIM_MATRIX
    to_label = set([int(qid[3:]) for qid, _ in QUESTION_POOL])
    row = SIM_MATRIX[rowidx]
    ranked_neighbors = []
    for idx, dist in enumerate(row):
        if idx == rowidx:
            continue
        if idx not in to_label:
            continue
        ranked_neighbors.append((idx, dist))
    ranked_neighbors = sorted(ranked_neighbors, key=lambda x: x[1], reverse=True)
    return ranked_neighbors


def get_random_candidate():
    if len(QUESTION_POOL) == 0:
        return (-1, "All Questions are Annotated!")
    random.seed(42)
    tmp = [(x, y) for x, y in QUESTION_POOL.items()]
    random.shuffle(tmp)
    return tmp[0]


def remove_questions_from_pool(toremove):
    global QUESTION_POOL
    question_pool_new = dict()
    for qid, question in QUESTION_POOL.items():
        if qid not in toremove:
            question_pool_new[qid] = question
    QUESTION_POOL = question_pool_new


""" Web Service Code """


@app.before_first_request
def initialize():
    print("INITIALIZE")
    global ALREADY_LABELED, QUESTION_POOL, QUESTION_POOL_ANNOT, SIM_MATRIX, CSVpath
    ALREADY_LABELED = set()
    QUESTION_POOL = load_questions(config.PATH_QUESTIONS)  # [(QID1, QuestionText1), ..., (QIDN, QuestionTextN)]
    SIM_MATRIX = np.loadtxt(config.PATH_SIM_MATRIX)
    assert len(QUESTION_POOL) == SIM_MATRIX.shape[0] == SIM_MATRIX.shape[1]

    # schauen was bereits in file anotiert ist und aus Pool löschen
    annotated = list()
    QUESTION_POOL_ANNOT = dict()

    if not os.path.exists(os.path.dirname(CSVpath)):
        os.makedirs(os.path.dirname(CSVpath))

    with open(CSVpath, mode="a+", encoding="utf-8") as f:
        s = csv.reader(f, delimiter=",")
        # print(list(s)[0][2])
        # for idn, label, querry in s:
        for idn in s:
            # print(idn[1], idn[2])
            for num, line in QUESTION_POOL.items():
                if num == idn[0] and line == idn[2]:
                    # print("schon enthalten: %s", num, line)
                    annotated.append(num)
                    QUESTION_POOL_ANNOT[idn[0]] = idn[1], idn[2]
    print("already annotated in file:", annotated)
    # print(QUESTION_POOL.items())
    print("############################")
    # print(QUESTION_POOL_ANNOT.items())

    # Remove questions that were already annotated in file
    remove_questions_from_pool(set(annotated))


@app.route('/')
def index():
    candidate = get_random_candidate()
    return render_template('interface.html', name="Startpage", questions=QUESTION_POOL.items(), annotated_data=QUESTION_POOL_ANNOT.items())
    # annotated_data=QUESTION_POOL_ANNOT.items()


@app.route('/saveannotation', methods=['POST', 'GET'])
def saveannotation():
    global QUESTION_POOL
    global QUESTION_POOL_ANNOT
    global CSVpath
    try:
        label = request.form.get('label')
        question_ids = request.form.getlist('questionlist')
        print("##############################")
        print("{:10s}".format("Questions"), question_ids)
        print("{:10s}".format("Label"), label)
        print("##############################")

        # print("##############################")
        # Start writing to CSV
        s = csv.writer(open(CSVpath, "a", newline='', encoding="utf-8"), delimiter=",")
        for qid_html in question_ids:
            # print(qid_html)
            for qid, question in QUESTION_POOL.items():
                # print(qid, qid_html, question)
                if qid_html == qid:
                    # print("bin in if")
                    tex = question.strip()
                    s.writerow([qid, label, tex])
                    # QUESTION_POOL_CSV[qid]=label, tex
                    QUESTION_POOL_ANNOT[qid] = label, tex
        # End writing to CSV

        # Remove questions that were already annotated from our pool
        remove_questions_from_pool(set(question_ids))

    except Exception as e:
        print("Something went wrong!")
        print(e)
    return index()


@app.route('/relabel', methods=['POST', 'GET'])
def relabel():
    global QUESTION_POOL_ANNOT
    global CSVpath
    try:
        newlabel = request.form.get('newlabel')
        annotation_ids = request.form.getlist('annotationlist')
        for qid_html in annotation_ids:
            # print(qid_html)
            # for Qestion-Id, label, text
            for qid, question in QUESTION_POOL_ANNOT.items():
                # print(qid, qid_html, question)
                if qid_html == qid:
                    # print("bin in if - Label ändern")
                    # QUESTION_POOL_CSV[qid]=newlabel, tex
                    QUESTION_POOL_ANNOT[qid] = newlabel, question[1]

        # CSV Datei neu beschreiben:
        s = csv.writer(open(CSVpath, "w", newline='', encoding="utf-8"), delimiter=",")
        s.writerow(["Qestion ID", "Label", "Query"])
        # print(QUESTION_POOL_ANNOT.items())
        for qid, question in QUESTION_POOL_ANNOT.items():
            # print(qid, question[0], question[1])
            s.writerow([qid, question[0], question[1]])
    except Exception as e:
        print("Something went wrong!")
        print(e)
    return index()


@app.route('/test')
def test():
    print("hallo")
    return "<h1>hallo</h1>"


@app.route('/reset', methods=['POST', 'GET'])
def reset():
    global CSVpath
    # reset the Anotation File
    print("reset the annotation File")
    s = csv.writer(open(CSVpath, "w", newline='', encoding="utf-8"), delimiter=",")
    s.writerow(["Qestion ID", "Label", "Query"])
    initialize()
    return index()


if __name__ == '__main__':
    app.run()
