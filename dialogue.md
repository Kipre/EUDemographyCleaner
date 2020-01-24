# Dialogue in NLP

__Cyprien NEVEROV - January 2020__

## Introduction

A _dialogue system_, or _conversational agent_ (CA), is a computer system intended to converse with a human. 
Dialogue systems employed one or more of text, speech, graphics and other modes for communication on both the input and output channel.

With the rising trend of artificial intelligence, more and more devices have incorporated goal-oriented spoken dialogue systems. 
Among popular virtual personal assistants, Microsoft’s Cortana, Apple’s Siri, Amazon Alexa, Google Assistant, and Facebook’s M, have incorporated dialogue system modules in various devices, which allow users to speak naturally in order to finish tasks more efficiently. 
The traditional conversational systems have rather complex and/or modular pipelines. 
The advance of deep learning technologies has recently risen the applications of neural models to dialogue modeling. 
Nevertheless, applying deep learning technologies for building robust and scalable dialogue systems is still a challenging task and an open research area as it requires deeper understanding of the classic pipelines as well as detailed knowledge on the benchmark of the models of the
prior work and the recent state-of-the-art work [1].

## Components

Basic components of a dialog system are:

1. automatic speech recognition (ASR); 
2. language understanding (LU);
3. dialogue management (DM);
4. natural language generation (NLG).

## Evaluation

Evaluating the quality of the generated response is an important aspect of dialogue response generation systems. 
Task-oriented dialogue system can be evaluated based on human-generated supervised signals, such as a task completion test or a user satisfaction score, however, automatically evaluating the quality of generated responses for non-task-oriented dialogue systems remains an open question due to the high response diversity. 
Despite the fact that word overlap metrics such as BLEU, METEOR, and ROUGE have been widely used to evaluate the generated responses, scholars found that those metrics, as well as word embedding metrics derived from word embedding models such as Word2Vec have either weak or no correlation with human judgements, although word embedding metrics are able to significantly distinguish between baselines and state-of-the-art models across multiple datasets.
[3] proposed to use two neural network models to evaluate a sequence of turn-level features to rate the success of a dialogue. 
[4] encoded the context, the true response and the candidate response into vector representations using RNN, and then computed a score using a dot-product between the vectors in a linearly transformed space. 
[5] combined referenced and unreferenced metrics, where the former measured the similarity between reply and the groundtruth through word embedding, and the latter scored the correlation between reply and query trained with a max-margin objective function, where the negative reply is randomly sampled. 
One promising approach comes from the idea of Turing test; employing an evaluator to distinguish machine-generated texts from human-generated ones. 
[6] and [7] explored adversarial evaluation model which assigns a score based on how easy it is to distinguish the generated responses from human responses, while [8] directly applied adversarial learning into dialogue generation. [2]

## Bibliography

1. Chen, Yun-Nung and Celikyilmaz, Asli and Hakkani-Tur, Dilek, [Deep Learning for Dialogue Systems](https://www.aclweb.org/anthology/P17-5004.pdf). _Proceedings of the 27th International Conference on Computational Linguistics: Tutorial Abstracts_. 2018, Santa Fe, New Mexico, USA, Association for Computational Linguistics.

2. H. Chen, X. Liu, D. Yin, and J. Tang, [A Survey on Dialogue Systems: Recent Advances and New Frontiers](https://arxiv.org/pdf/1711.01731.pdf). *arXiv preprint arXiv:1711.01731*, 2018.

3. P-H. Su, D. Vandyke, M. Gasic, D. Kim, N. Mrksic, T-H. Wen, and S. Young. [Learning from real users: Rating dialogue success with neural networks for reinforcement learning in spoken dialogue systems.](https://arxiv.org/abs/1508.03386) *arXiv
preprint arXiv:1508.03386*, 2015.

4. R. Lowe, M. Noseworthy, I. V. Serban, N. AngelardGontier, Y. Bengio, and J. Pineau. Towards an automatic turing test: Learning to evaluate dialogue responses. *In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1116–1126*, Vancouver, Canada, July 2017. Association for Computational Linguistics.

5. C. Tao, L. Mou, D. Zhao, and R. Yan. Ruber: An unsupervised method for automatic evaluation of open-domain dialog systems. *arXiv preprint arXiv:1701.03079*, 2017.

6. A. Kannan and O. Vinyals. Adversarial evaluation of dialogue models. *arXiv preprint arXiv:1701.08198*, 2017.

7. E. Bruni and R. Fernandez. Adversarial evaluation for open-domain dialogue generation. *In Proceedings of the 18th Annual SIGdial Meeting on Discourse and Dialogue, pages 284–288*, 2017.

8.  S. R. Bowman, L. Vilnis, O. Vinyals, A. M. Dai, R. Jozefowicz, and S. Bengio. Generating sentences from a continuous space. *In Proceedings of The 20th SIGNLL Conference on Computational Natural Language Learning*
