import pandas as pd
import config

class Answers:

    answers = None
    answer_ids = set()

    def __init__(self):
        self.initialize()

    def initialize(self):
        answers = []
        df = pd.read_csv(config.PATH_ANSWERS)
        for aid, answer in zip(df["aid"], df["answer"]):
            answers.append({"aid": aid, "answer": answer})
            self.answer_ids.add(aid)
        self.answers = answers

    def get_answer(self, aid):
        print(aid)
        for answer in self.answers:
            if answer["aid"] == aid:
                return answer
        assert False
        return None

    def add_answer(self, answer, answer_short):
        pass


    def check_valid_label(self, label):
        # if labels is None or len(labels) != 1:
        #     return False
        # label = labels[0]
        if label is None:
            return False
        if label in self.answer_ids:
            return True
        if label == "nolabel":
            return True
        return False