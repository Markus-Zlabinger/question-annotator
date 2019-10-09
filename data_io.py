import numpy as np
import config

def get_questions():
    questions = dict()
    with open(config.PATH_QUESTIONS, mode="r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            question_text = line.strip()
            if question_text:  # Ignore empty lines
                questions[str(index)] = question_text
    return questions

def get_sim_matrix():
    return np.loadtxt(config.PATH_SIM_MATRIX)

def get_question_vectors():
    return np.loadtxt(config.PATH_QUESTIONS_VECTORS)