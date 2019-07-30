from src.question import Question
from src.preprocessing import text2tokens

def load_questions(path):
    questions = dict()
    qidx = 0
    with open(path, mode="r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            question_text = line.strip()
            if question_text:  # Ignore empty lines
                questions[str(qidx)] = question_text
                qidx += 1
    return questions

    # Preprocess question text (i.e. tokenize, lowercasing, stemming, ...)
    # for question in questions:
    #     question.text_tokens = text2tokens(question.text)
    # return questions



def load_annotations(path):
    return set()

def load_embeedings(path):
    pass

def load_training_data(path):
    corpus = []
    with open(path, mode="r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if text:  # Ignore empty lines
                corpus.append(text)
    return corpus