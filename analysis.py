import defaultsettings
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS
from src.data_io import load_questions, load_annotations
import csv
import config
import random
import os
import numpy as np
import data_io
from pyclustering.cluster.elbow import elbow
from sklearn.decomposition import PCA
from pyclustering.cluster.silhouette import silhouette_ksearch_type, silhouette_ksearch
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import matplotlib.pyplot as plt
from sklearn.cluster import *
from sklearn.cluster import OPTICS
from tqdm import tqdm
import pickle
from sklearn.manifold import TSNE
from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster import cluster_visualizer
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import FCPS_SAMPLES
import annotator
import pandas as pd
from sklearn.metrics.cluster import *
import random
from sklearn.feature_extraction.text import TfidfVectorizer


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

