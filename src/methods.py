import numpy as np
import warnings
from collections import Counter
from sklearn.decomposition import TruncatedSVD


class Sif:
    document_frequencies = None
    word2weight = None
    n_components = 1  # Same parameter as in the paper
    show_warnings = None
    pc = None
    a = 1e-3  # Same parameter as in the paper
    is_fit = False
    embedding_vocab = None

    def __init__(self, embedding_vocab, show_warnings=True, a=1e-3, n_components=1):
        self.embedding_vocab = embedding_vocab
        self.a = a
        self.n_components = n_components
        self.show_warnings = show_warnings

    def fit(self, tokenlists):
        self.word2weight = self.get_w2weight_dict(tokenlists)
        mat = self.get_embeddings(tokenlists, ignore_empty=True)
        self.compute_principal_components(mat)
        self.is_fit = True

    def transform(self, tokenlists):
        if self.is_fit == False:
            raise Exception("You have to fit the model first before using this function.")

        sentence_embeddings = self.get_embeddings(tokenlists, ignore_empty=False)

        if self.n_components > 0:
            sentence_embeddings = self.remove_principal_component(sentence_embeddings, n_components=self.n_components)
        return sentence_embeddings

    def get_embeddings(self, tokenlists, ignore_empty):
        weights = [[] for _ in range(len(tokenlists))]
        word_embedding_lists = [[] for _ in range(len(tokenlists))]
        for i, tokenlist in enumerate(tokenlists):
            for token in tokenlist:
                if token in self.word2weight and token in self.embedding_vocab:
                    weights[i].append(self.word2weight[token])
                    word_embedding_lists[i].append(self.embedding_vocab[token])
                else:
                    if self.show_warnings:
                        warnings.warn("Token was not found in the vocabulary: {}".format(token))

        # Compute Weighted Sentence Embeddings
        sentence_embeddings = []
        for i, (word_embedding_list, weight_list) in enumerate(zip(word_embedding_lists, weights)):
            if len(word_embedding_list) == 0:
                if ignore_empty:
                    continue
                else:
                    averaged_vector = np.zeros(self.embedding_vocab.vector_size)  # Take a [0.0, ..., 0.0] vector for texts that cannot be mapped to an embedding
            else:
                averaged_vector = np.average(word_embedding_list, axis=0, weights=weight_list)
            sentence_embeddings.append(averaged_vector)

        # sentence_embeddings = []
        # for i, word_embedding_list in enumerate(word_embedding_lists):
        #     sentence_embedding = None
        #     for j, word_embedding in enumerate(word_embedding_list):
        #         if j == 0:
        #             sentence_embedding = np.array(word_embedding) * weights[i][j]
        #         else:
        #             sentence_embedding += np.array(word_embedding) * weights[i][j]
        #     if len(word_embedding_list) == 0:
        #         if ignore_empty:
        #             continue
        #         else:
        #             sentence_embedding = np.zeros(self.embedding_vocab.vector_size)  # Take a [0.0, ..., 0.0] vector for texts that cannot be mapped to an embedding
        #     else:
        #         sentence_embedding /= len(word_embedding_list)
        #     sentence_embeddings.append(sentence_embedding)
        sentence_embeddings = np.array(sentence_embeddings)
        return sentence_embeddings



    def get_w2weight_dict(self, tokenlists):
        tokens_flat = []

        # Compute term frequency
        for tokenlist in tokenlists:
            tokens_flat.extend(list(tokenlist))
        word2weight = Counter(tokens_flat)

        # Normalize term frequency
        denominator = len(tokens_flat)


        # Compute weights for each term
        for key, value in word2weight.items():
            word2weight[key] = self.a / (self.a + value / denominator)
        return dict(word2weight)

    def compute_principal_components(self, mat, n_components=1):
        if self.pc is None:
            svd = TruncatedSVD(n_components=n_components, n_iter=7, random_state=0)
            svd.fit(mat)
            self.pc = svd.components_
        else:
            raise Exception("PCs were already computed!")

    def remove_principal_component(self, mat, n_components=1):
        """
        NOTE: Code taken from the official SIF implementation
        :param mat: n x m matrix
        :param n_components: number of components to remove
        :return: n x m matrix in which the projections of the first n_components are removed
        """

        # Remove principal component
        if self.pc is None:
            raise Exception("The PCs must be computed first!")

        if n_components == 1:
            mat_pc = mat - mat.dot(self.pc.transpose()) * self.pc
        else:
            mat_pc = mat - mat.dot(self.pc.transpose()).dot(self.pc)
        return mat_pc
