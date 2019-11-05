import data_io
import random
import pandas as pd
import os
import config
from collections import Counter
import numpy as np
from itertools import combinations


class Annotator:
    questions = None
    question_pool = None
    # sim_matrix = None
    question_ids = None
    q2q_simmat = None


    group_counter = 0

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.questions = data_io.get_questions()
        # self.sim_matrix = data_io.get_sim_matrix(config.PATH_SIM_MATRIX)
        self.q2q_simmat = data_io.get_q2q_simmatrix()
        self.q2s_simmat = data_io.get_q2s_simmatrix()
        self.initialize_question_pool()
        self.initialize_counter()

    def get_q2q_similarity(self, qid1, qid2):
        return self.q2q_simmat.loc[str(qid1), str(qid2)]

    def get_q2a_similarity(self, qid, aid):
        return self.q2s_simmat.loc[str(qid), str(aid)]

    def initialize_question_pool(self):
        self.question_pool = dict()
        annotations = self.get_annotations()

        if annotations is not None:
            toremove_qids = annotations["qid"].tolist()
            for qid, question in self.questions.items():
                if qid not in toremove_qids:
                    self.question_pool[qid] = question
        else:
            self.question_pool = {qid: question for qid, question in self.questions.items()}

    def initialize_counter(self):
        annotations = self.get_annotations()
        if annotations is not None:
            self.group_counter = int(annotations["group"].max()) + 1

    # Returns a list of similar questions (neighbors) with respect to a query question
    def get_ranked_neighbors(self, qid):
        yet_to_annotate = set(self.question_pool.keys())
        row = self.q2q_simmat.loc[qid].copy()
        ranked_neighbors = []

        for idx, sim in zip(row.index, row):
            if idx == qid:
                continue
            if idx not in yet_to_annotate:
                continue
            ranked_neighbors.append((idx, sim))

        # for idx, dist in row:
        #     if idx == qid:
        #         continue
        #     if idx not in yet_to_annotate:
        #         continue
        #     ranked_neighbors.append((idx, dist))
        ranked_neighbors = sorted(ranked_neighbors, key=lambda x: x[1], reverse=True)
        return ranked_neighbors

    def get_similar_questions(self, candidate, preselect_ids=set()):
        # Case: All questions are already annotated
        if candidate is None:
            return []
        candidate_qid = candidate["qid"]
        questionlist = []
        ranked_neighbors = self.get_ranked_neighbors(candidate_qid)
        for qid, similarity in ranked_neighbors:
            question = self.get_question(qid)
            question["similarity"] = similarity
            question["preselect"] = qid in preselect_ids
            questionlist.append(question)
        return questionlist

    def get_questionpool(self, questions):
        annotations = self.get_annotations()
        if annotations is not None:
            toremove_qids = annotations["qid"].tolist()
            return self.remove_questions_from_pool(toremove_qids)
        return questions

    def remove_questions_from_pool(self, toremove_qids):
        toremove_qids = set(toremove_qids)
        questionpool_new = dict()
        for qid, question in self.question_pool.items():
            if qid not in toremove_qids:
                questionpool_new[qid] = question
        self.question_pool = questionpool_new

    def get_annotations(self):
        if not os.path.isfile(config.PATH_ANNOTATION_FILE):
            return None
        df = pd.read_csv(config.PATH_ANNOTATION_FILE, dtype={"qid": str, "aid": str})
        # print(df["qid"])
        return df

    def get_overview(self, sort_by, answer_catalog):
        annotations = self.get_annotations()
        if annotations is None:
            return []

        question_groups = []

        qid2outlier = self.compute_outliers(annotations)
        for group in annotations[sort_by].unique():
            annotations[annotations[sort_by] == group]
            df = annotations[annotations[sort_by] == group]
            aids = df["aid"].unique()
            assert len(aids) == 1
            aid = aids[0]

            answer = answer_catalog.get_answer(aid)

            # questions = []
            # for qid, aid in zip(df["qid"], df["aid"]):

            questions = [self.get_question(q) for q in df["qid"]]

            for question in questions:
                question["outlier"] = qid2outlier[(question["qid"], aid)]

            question_groups.append(
                {
                    "answer": answer,
                    "questions": questions,
                }
            )
        return question_groups

    def compute_outlier_score(self, qid_current, qids):
        assert qid_current not in qids
        scores = [self.get_q2q_similarity(qid_current, qid) for qid in qids]
        return np.median(scores)


    def compute_outliers(self, annotations):
        answer_labels = list(annotations["aid"].unique())
        answer_label2qids = {aid: set(annotations["qid"][annotations["aid"] == aid]) for aid in answer_labels}
        outlier_scores = dict()
        for qid_current, aid_current in zip(annotations["qid"], annotations["aid"]):
            ranked_scores = []
            for answer_label in answer_labels:
                qids = answer_label2qids[answer_label]
                if qid_current not in qids:
                    score_other_aid = self.compute_outlier_score(qid_current, qids)
                    ranked_scores.append({"score": score_other_aid, "aid": answer_label})
            ranked_scores = sorted(ranked_scores, key=lambda x: x["score"], reverse=True)


            other_qids = answer_label2qids[aid_current]
            score_current = 1.0
            if len(other_qids) > 1: # Check if current_qid is the only question labeled with current_aid
                score_current = self.compute_outlier_score(qid_current, answer_label2qids[aid_current]- {qid_current})
            second_best_score = 0.0
            second_best_aid = aid_current
            if len(ranked_scores) > 0:
                second_best_score = ranked_scores[0]["score"]
                second_best_aid = ranked_scores[0]["aid"]

            outlier_scores[(qid_current, aid_current)] = {"score": score_current - second_best_score, "predicted_label": second_best_aid, "initial_label": aid_current}
            # score_current_aid = self.get_q2q_similarity(qid_current, qid_current)
            # score_other_aid_max = 0.0
            # other_aid_max = aid_current
            # other_qids = [x for x in aid2qids[aid_current] if x != qid_current]
            # if len(other_qids) > 0: # Check if current_qid is the only question labeled with current_aid
            #     score_current_aid = self.compute_outlier_score(qid_current, aid2qids[aid_current])
            # for aid in aids:
            #     qidlist = aid2qids[aid]
            #     if qid_current not in qidlist:
            #         score_other_aid = self.compute_outlier_score(qid_current, qidlist)
            #         if score_other_aid_max < score_other_aid:
            #             score_other_aid_max = score_other_aid
            #             other_aid_max = aid

        return outlier_scores



    def save_annotations(self, aid, question_ids):
        annotations = []
        for qid in question_ids:
            annotations.append({
                "aid": aid,
                "qid": qid,
                "question": self.questions[qid],
                "group": self.group_counter,
            })
        self.group_counter += 1
        df = pd.DataFrame(annotations, dtype=str)

        # Save Annotations
        append_header = True
        if os.path.isfile(config.PATH_ANNOTATION_FILE):
            append_header = False
        df.to_csv(config.PATH_ANNOTATION_FILE, index=False, mode='a', header=append_header)

    def modify_annotation(self, qid, answerlabels):
        for answerlabel in answerlabels:
            self.delete_annotation(qid, answerlabel)
        for aid in answerlabels:
            self.save_annotations(aid, [qid])
        pass

    # def remove_annotation(self, qid):
    #     annotations = self.get_annotations()
    #     if annotations is not None:
    #         annotations = annotations[annotations["qid"] != qid]
    #         # Save
    #         annotations.to_csv(config.PATH_ANNOTATION_FILE, index=False, mode='w', header=True)
    def delete_annotation(self, qid, aid):
        annotations = self.get_annotations()
        if annotations is not None:
            annotations = annotations[(annotations["qid"] != qid) | (annotations["aid"] != aid)].copy()
            # Save
            annotations.to_csv(config.PATH_ANNOTATION_FILE, index=False, mode='w', header=True)
            self.initialize_question_pool()


    def reset(self):
        if os.path.isfile(config.PATH_ANNOTATION_FILE):
            os.remove(config.PATH_ANNOTATION_FILE)
        return Annotator()

    def get_question(self, qid):
        return {
            "qid": qid,
            "question": self.questions[qid],
            # "preselect": False # TODO: make dynamic
        }

    def get_random_candidate(self):
        if len(self.question_pool) == 0:
            return None
        random.seed(42)
        tmp = [x for x, _ in self.question_pool.items()]
        random.shuffle(tmp)
        return self.get_question(tmp[0])

    def get_next_candidate(self):
        if len(self.question_pool) == 1:
            return self.get_question(list(self.question_pool.keys())[0])

        if len(self.question_pool) == 0:
            return None

        max_sim = -100.0
        representative_idx = None
        pairs = combinations(self.question_pool.keys(), 2)
        for qid1, qid2 in pairs:
            cur_sim = self.get_q2q_similarity(qid1, qid2)
            if cur_sim > max_sim:
                representative_idx = qid1
                max_sim = cur_sim
        return self.get_question(representative_idx)


        # Sort all_distances ascending
        # tmp = sorted(all_distances, key=lambda x: x[2], reverse=True)
        # highest_similarity = tmp[0][2]  # this is the minimum distance
        #
        # # When multiple question pairs have the 'highest_similarty' take the one that occurs more often
        # count = Counter()
        # for idx1, idx2, d in tmp:
        #     if d != highest_similarity:
        #         break  # We can break as soon as the first distance is smaller since we sorted ascending
        #     count[idx1] += 1
        #     count[idx2] += 1
        #
        # representative_idx = count.most_common(1)[0][0]

