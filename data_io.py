import numpy as np


def get_questions(path):
    questions = dict()
    # questions = list()
    with open(path, mode="r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            question_text = line.strip()
            if question_text:  # Ignore empty lines
                questions[index] = question_text
                # questions.append(question_text)
    return questions

def get_sim_matrix(path):
    return np.loadtxt(path)

def get_question_vectors(path):
    return np.loadtxt(path)