import defaultsettings
from flask import Flask, render_template
from src.data_io import load_questions, load_annotations
from gensim.parsing.preprocessing import preprocess_documents
from src.preprocessing import text2tokens
import config
import pickle

app = Flask(__name__)


""" Global Variables """
ALREADY_LABELED = None
QUESTION_POOL = None


def initialize():
    global ALREADY_LABELED
    global QUESTION_POOL

    # Load questions
    QUESTIONS = load_questions(config.PATH_QUESTIONS)

    # Preprocess question text (i.e. tokenize, lowercasing, stemming, ...)
    for question in QUESTIONS:
        question.text_tokens = text2tokens(question.text)

def render_canditate(question):
    ALREADY_LABELED.add(question.qid) # Remove

    return render_template("index.html", candidate=question.text)

@app.route('/')
def get_next_candidate():
    for question in QUESTION_POOL:
        if question.qid not in ALREADY_LABELED:
            return render_canditate(question)
    return "All Questions were Annotated!"



    # return ""
    # return render_candidate()
    # # return render_template("index.html", candidate="candidate")
    # # return 'Hello, World!'

# @app.route('/annotate/')
# def render_candidate():
#     return render_template("index.html", candidate=candidate)



if __name__ == '__main__':
    pass
initialize()



    # ALREADY_LABELED = load_annotations() # Load annotations from previous launches
    # questions = load_questions("./data/sample-questions.txt")
    # app.run()
    # render_candidate(questions[0].text)

    # for question in questions:
    #     pass



# questions[-1]
