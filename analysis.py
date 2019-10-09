import defaultsettings
from flask import Flask, redirect, url_for, request, render_template
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
from sklearn.cluster import KMeans
from tqdm import tqdm
import pickle
from sklearn.manifold import TSNE
from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster import cluster_visualizer
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import FCPS_SAMPLES

app = Flask(__name__)

# https://github.com/annoviko/pyclustering/issues/416

# Load Global Variables
QUESTIONS = np.array(data_io.get_questions())
QUESTIONS_VECTORS = data_io.get_question_vectors()
SIM_MATRIX = data_io.get_sim_matrix()

##
# vecs = PCA(n_components=40, random_state=0).fit_transform(QUESTIONS_VECTORS)
# kmin, kmax = 2, int(len(QUESTIONS)/2)
# elbow_instance = elbow(vecs, kmin, kmax).process()
# amount_clusters = elbow_instance.get_amount()
#
# print(amount_clusters)
#
# ##
# # Load list of points for cluster analysis.
# # sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)
#
# # Set random initial medoids.
# initial_centers = list(range(amount_clusters))
#
# # Create instance of K-Medoids algorithm.
# kmedoids_instance = kmedoids(QUESTIONS_VECTORS, initial_centers)
# # Run cluster analysis and obtain results.
# kmedoids_instance.process()
# clusters = kmedoids_instance.get_clusters()
# # Show allocated clusters.
# print(clusters)
# # Display clusters.
# visualizer = cluster_visualizer()
# vecs = TSNE(n_components=2, random_state=42).fit_transform(QUESTIONS_VECTORS)
# visualizer.append_clusters(clusters, vecs)
# visualizer.show()
##
clusterer = KMeans(n_clusters=10)
clusterer.fit(vecs)
clusters = clusterer.labels_

cluster_results = []

for cluster in set(clusters):
    cluster_questions = QUESTIONS[cluster == clusters]
    cluster_result = {
        "cluster": cluster,
        "questions": list(cluster_questions),
        "representive": "TODO",
        "score": 0.0
    }
    cluster_results.append(cluster_result)
print(cluster_results)
# for question, cluster in zip(QUESTIONS, clusters):
#
#     result =

@app.route('/getclusters')
def get_clusters():
    return [{'cluster': 0, 'questions': ['Hello my friend', 'I wish you a great day', 'What to do if mobile is lost?', 'Mobilephone stolen', 'Where should I buy a new phone???', 'where can i find my login credentials', 'login details lost, where to get new ones?', 'request new login credentials', 'what to do if password forgotten', 'do you have any special offers for long time customer', 'customer over years any offers', "I'm a loyal customer can you give me stuff for free", 'can i get a special offer for a phone', 'do you have an overview of offers', 'the power button does not work anymore', 'dark display and no power', 'Where can I get my e-mails online?', 'Online service for emails', 'web service for mails', 'Can I see my e-mails online??', 'Url for the e-mail webservice', 'How much do I pay for roaming'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 1, 'questions': ['password cannot remember', "can't remember password and login"], 'representive': 'TODO', 'score': 0.0}, {'cluster': 2, 'questions': ["I've lost my phone how get back", 'My mobile phone is gone', 'Someone has taken my phone out of my pocket yesterday', 'Thief has taken phone', 'Where best buy phone', 'Place for new phones', 'Mobile phone shopping', 'Buy mobile phone online', 'Can you recommend shopfs for mobile phones?', 'My phone is not working', 'cannot start phone', 'Since yesterday my phone has stopped working', 'Why is my mobile phone not working', 'HELP phone start fails'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 3, 'questions': ['Greeting'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 4, 'questions': ['special offers', 'special bonus program'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 5, 'questions': ['password forgotten', 'lost password'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 6, 'questions': ['emails online', 'e-mail online', 'online mails'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 7, 'questions': ['roaming overview prices', 'roaming per country'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 8, 'questions': ['webmail'], 'representive': 'TODO', 'score': 0.0}, {'cluster': 9, 'questions': ['phone dead'], 'representive': 'TODO', 'score': 0.0}]

##

##

# wce = elbow_instance.get_wce()
#
#
# plt.plot(range(2, len(wce)+2, 1), wce, 'bx-')
# plt.show()
##


##

# def elbow_method(data, K):
#     sum_of_squared_distances = []
#     for k in tqdm(K):
#         km = KMeans(n_clusters=k)
#         km = km.fit(data)
#         sum_of_squared_distances.append(km.inertia_)
#
#     plt.plot(K, sum_of_squared_distances, 'bx-')
#     plt.xlabel('k')
#     plt.ylabel('Sum_of_squared_distances')
#     plt.xticks(K)
#     plt.title('Elbow Method For Optimal k')
#     plt.show()
# tmp = TSNE(n_components=3, random_state=42).fit_transform(QUESTIONS_VECTORS)
# # vecs = PCA(n_components=5, random_state=0).fit_transform(QUESTIONS_VECTORS)
# K = list(range(1,20,1))
# elbow_method(tmp, K)
#
# elbow_instance = elbow(vecs, kmin, kmax).process()
# amount_clusters = elbow_instance.get_amount()
# print(amount_clusters)

##

# from pyclustering.samples.definitions import FCPS_SAMPLES
# from pyclustering.utils import read_sample
# sample = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)
# search_instance = silhouette_ksearch(QUESTIONS_VECTORS, 2, 10, algorithm=silhouette_ksearch_type.KMEANS).process()
#
# amount = search_instance.get_amount()
# scores = search_instance.get_scores()
# print(scores)
# print(amount)

# if __name__ == '__main__':
#     app.run()
