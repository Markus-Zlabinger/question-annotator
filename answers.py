import pandas as pd
import config
import data_io
from collections import defaultdict
import numpy as np


class Answers:
    answers = None
    answer_ids = None
    q2s_simmat = None
    aggregation_method = lambda x: np.max(x)

    def __init__(self):
        self.initialize()

    def initialize(self):
        answers = []
        answer_ids = []
        df = pd.read_csv(config.PATH_ANSWERS)
        for aid, answer in zip(df["aid"], df["answer"]):
            answers.append({"aid": aid, "answer": answer})
            answer_ids.append(aid)
        self.answers = answers
        self.answer_ids = answer_ids
        self.q2s_simmat = data_io.get_q2s_simmatrix()

    def get_answer(self, aid):
        # print(aid)
        for answer in self.answers:
            if answer["aid"] == aid:
                return answer
        assert False
        return None

    def add_answer(self, answer, answer_short):
        pass

    def get_ranked_answers(self, qids):
        if len(qids) == 0:
            ret = self.answers.copy()
            for x in ret:
                x["similarity"] = 0.0
            return ret

        answer2scores = defaultdict(list)
        for qid in qids:
            answers = self.q2s_simmat.loc[qid]
            for aid, simlist in zip(answers.index, answers):
                # print(aid, max(simlist))
                # pass
                answer2scores[aid].append(np.max(simlist))
        answer2scores = dict(answer2scores)

        ranked_answers = []
        for aid, scores in answer2scores.items():
            # TODO Fix aggregation

            # agg_score = self.aggregation_method(scores)
            agg_score = np.max(scores)
            ranked_answers.append({"aid": aid, "answer": self.get_answer(aid)["answer"], "similarity": agg_score})
        ranked_answers = sorted(ranked_answers, key=lambda x: x["similarity"], reverse=True)
        return ranked_answers


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
