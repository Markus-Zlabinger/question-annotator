from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS
import csv
import config
import random
import os
import numpy as np
import data_io
from sklearn.cluster import OPTICS
import pickle
import annotator
import pandas as pd
import random


class Analysis:
    questions = None
    questions_vectors = None

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.questions = list(data_io.get_questions(config.PATH_QUESTIONS).values())
        self.questions_vectors = data_io.get_question_vectors(config.PATH_QUESTIONS_VECTORS)


    def get_clusters(self):
        clusterer = OPTICS(metric="cosine", min_samples=3, algorithm="brute")
        clusterer.fit(self.questions_vectors)
        return self.prepare_clusters(clusterer.labels_)

    def prepare_clusters(self, cluster_labels):
        cluster_results = []
        questions = np.array(self.questions)
        score = 0.0
        # cluster_labels = np.array(cluster_labels)
        # clusters = set(cluster_labels)
        for cluster in set(cluster_labels):
            cluster_questions = questions[cluster_labels == cluster]
            cluster_result = {
                "cluster": int(cluster),
                "questions": list(cluster_questions),
                "representive": "TODO",
                "score": score
            }
            score += 1.0
            cluster_results.append(cluster_result)
        cluster_results = sorted(cluster_results, key = lambda x: x["score"], reverse=True)
        return cluster_results

