import pandas as pd
import config

class Answers:

    answers = None

    def __init__(self):
        self.initialize()

    def initialize(self):
        answers = dict()
        df = pd.read_csv(config.PATH_ANSWERS)
        for aid, answer in zip(df["aid"], df["answer"]):
            answers[aid] = answer
        self.answers = answers

    def check_valid_label(self, label):
        # if labels is None or len(labels) != 1:
        #     return False
        # label = labels[0]
        if label is None:
            return False
        if label in self.answers:
            return True
        if label == "nolabel":
            return True
        return False