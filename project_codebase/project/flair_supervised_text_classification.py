# -*- coding: utf-8 -*-

import os

from flair.data import Corpus
from flair.datasets import ClassificationCorpus
from flair.embeddings import CamembertEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from torch.optim import Adam

data_folder = './data/corpus_splits/'

# column format indicating which columns hold the text and label(s)
column_name_map = {1: "text", 2: "label_topic", }

# Camembert
camembert = CamembertEmbeddings(layers="-1,-2,-3,-4")

embedding_list = [camembert]

# Document embedding model
document_embeddings = DocumentRNNEmbeddings(embedding_list, hidden_size=750, bidirectional=True,
                                            rnn_layers=2,
                                            rnn_type='GRU',
                                            dropout=0.4,
                                            word_dropout=0.1)

# 10-fold cross validation
for root, dirs, files in os.walk(data_folder):
    for dir in dirs:
        if "split" in dir:
            print("Processing " + dir + " ...")
            corpus: Corpus = ClassificationCorpus(data_folder + "/" + dir,
                                                  test_file='test.txt',
                                                  dev_file='dev.txt',
                                                  train_file='train.txt', in_memory=True)

            classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(),
                                        multi_label=False)
            trainer = ModelTrainer(classifier, corpus)
            model_path = data_folder + "/" + dir + "/model/"
            scores = trainer.train(model_path, max_epochs=50,
                                   embeddings_storage_mode="cpu",
                                   learning_rate=0.3,
                                   mini_batch_size=32,
                                   anneal_factor=0.5,
                                   shuffle=False,
                                   patience=5, save_final_model=False, anneal_with_restarts=False)
#            expected = [sentence.labels[0].value for sentence in corpus.test.sentences]
#            predictions = [sentence.labels[0].value for sentence in classifier.predict(corpus.test.sentences)]
#            print(accuracy(expected, predictions))
