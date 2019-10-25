import data_io
import random
import pandas as pd
import os
import config
from collections import Counter
import numpy as np


class Annotator:
    questions = None
    question_pool = None
    sim_matrix = None

    group_counter = 0

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.questions = data_io.get_questions()
        self.sim_matrix = data_io.get_sim_matrix(config.PATH_SIM_MATRIX)
        self.initialize_question_pool()
        self.initialize_counter()

    def initialize_question_pool(self):
        self.question_pool = dict()
        annotations = self.get_annotations()

        if annotations is not None:
            toremove_qids = annotations["qid"].tolist()
            for qid, question in enumerate(self.questions):
                if qid not in toremove_qids:
                    self.question_pool[qid] = question
        else:
            self.question_pool = {qid: question for qid, question in enumerate(self.questions)}

    def initialize_counter(self):
        annotations = self.get_annotations()
        if annotations is not None:
            self.group_counter = int(annotations["group"].max()) + 1

    # Returns a list of similar questions (neighbors) with respect to a query question
    def get_ranked_neighbors(self, qid):
        yet_to_annotate = set(self.question_pool.keys())
        row = self.sim_matrix[qid]
        ranked_neighbors = []
        for idx, dist in enumerate(row):
            if idx == qid:
                continue
            if idx not in yet_to_annotate:
                continue
            ranked_neighbors.append((idx, dist))
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
        return pd.read_csv(config.PATH_ANNOTATION_FILE)

    def get_overview(self, sort_by, answer_catalog):
        if not os.path.isfile(config.PATH_ANNOTATION_FILE):
            return []
        annotations = pd.read_csv(config.PATH_ANNOTATION_FILE)
        question_groups = []

        qid2outlier = self.compute_outliers(annotations)

        for group in annotations[sort_by].unique():
            annotations[annotations[sort_by] == group]
            df = annotations[annotations[sort_by] == group]
            aids = df["label"].unique()
            assert len(aids) == 1
            aid = aids[0]

            answer = answer_catalog.get_answer(aid)
            questions = [self.get_question(q) for q in df["qid"]]

            for question in questions:
                question["outlier"] = qid2outlier[question["qid"]]

            question_groups.append(
                {
                    "answer": answer,
                    "questions": questions,
                }
            )
        return question_groups

    def compute_outlier_score(self, qid_current, qids):
        scores = [self.sim_matrix[qid_current, qid] for qid in qids]
        return np.mean(scores)


    def compute_outliers(self, annotations):
        labels = list(annotations.label.unique())
        label2qids = {label: list(annotations["qid"][annotations.label == label]) for label in labels}
        outlier_scores = dict()
        for qid_current, label_current in zip(annotations["qid"], annotations["label"]):
            score_current_label = self.sim_matrix[qid_current, qid_current]
            score_other_label_max = 0.0
            other_label_max = label_current
            other_qids = [x for x in label2qids[label_current] if x != qid_current]
            if len(other_qids) > 0: # Check if current_qid is the only question labeled with current_label
                score_current_label = self.compute_outlier_score(qid_current, label2qids[label_current])
            for label in labels:
                if label != label_current:
                    score_other_label = self.compute_outlier_score(qid_current, label2qids[label])
                    if score_other_label_max < score_other_label:
                        score_other_label_max = score_other_label
                        other_label_max = label
            outlier_scores[qid_current] = {"score": score_current_label - score_other_label_max, "predicted_label": int(other_label_max), "initial_label": label_current}
        return outlier_scores

    def save_annotations(self, label, question_ids):
        # Check if IDs were already annotated
        question_ids_clean = []
        for qid in question_ids:
            if qid in self.question_pool:
                question_ids_clean.append(qid)
        question_ids = question_ids_clean
        # Prepare Annotations
        annotations = []
        for qid in question_ids:
            annotations.append({
                "label": label,
                "qid": qid,
                "question": self.questions[qid],
                "group": self.group_counter,
            })
        self.group_counter += 1

        # Save Annotations
        append_header = True
        if os.path.isfile(config.PATH_ANNOTATION_FILE):
            append_header = False
        df = pd.DataFrame(annotations)
        df.to_csv(config.PATH_ANNOTATION_FILE, index=False, mode='a', header=append_header)

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
        dmatrix = self.sim_matrix
        all_distances = []
        for rowidx, row in enumerate(dmatrix):
            if rowidx not in self.question_pool:
                continue
            for colidx, d in enumerate(row):
                if colidx not in self.question_pool:
                    continue
                if rowidx == colidx:
                    continue
                if rowidx > colidx:
                    continue
                idx1 = min(colidx, rowidx)
                idx2 = max(colidx, rowidx)
                all_distances.append((idx1, idx2, d))

        if len(all_distances) == 0:
            # In case that only one question remains to annotate
            if len(self.question_pool) == 1:
                return self.get_question(list(self.question_pool.keys())[0])
            return None

        # Sort all_distances ascending
        tmp = sorted(all_distances, key=lambda x: x[2], reverse=True)
        highest_similarity = tmp[0][2]  # this is the minimum distance

        # When multiple question pairs have the 'highest_similarty' take the one that occurs more often
        count = Counter()
        for idx1, idx2, d in tmp:
            if d != highest_similarity:
                break  # We can break as soon as the first distance is smaller since we sorted ascending
            count[idx1] += 1
            count[idx2] += 1

        representative_idx = count.most_common(1)[0][0]
        return self.get_question(representative_idx)
