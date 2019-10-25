import numpy as np
import config


def get_questions(path=config.PATH_QUESTIONS):
    # questions = dict()
    questions = list()
    with open(path, mode="r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            question_text = line.strip()
            if question_text:
                questions.append(question_text)
            # if question_text:  # Ignore empty lines
            #     questions[index] = question_text
                # questions.append(question_text)
    return questions

def get_sim_matrix(path):
    return np.loadtxt(path)

def get_question_vectors(path=config.PATH_QUESTIONS_VECTORS):
    return np.loadtxt(path)