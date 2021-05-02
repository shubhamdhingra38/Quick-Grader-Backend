This is the backend for http://quick-grader-v2.herokuapp.com/

The frontend repository containing the react code can be found here: 

Backend Frameworks:
1. Django
2. Django Rest Framework

### Motivation and Methodology
I tried to cluster text using traditional natural language processing techniques (such as TF-IDF), then assigning the same score to every point in the cluster as the score of centroid of the cluster.

I looked at Kappa scores for different combination of preprocessing techniques and algorithms used for clustering. Then I tried using word embeddings, followed by Universal Sentence Encoder which transforms the entire sentence into a vector as compared to word embeddings which give vectors only word by word. The performance of Universal Sentence Encoder was found to be the best (other related stuff like BERT gave similar score).

Dataset used: https://www.kaggle.com/c/asap-sas

It has two human scorers, with their Kappa score being `~ 0.9`

Using the dataset, on an average a Kappa score of `~ 0.5` can be achieved (averaged over the 10 essays in the dataset). For this, the teacher only needs to grade `20%` of the total responses. A further improvement to this score can be by allowing teachers to observe word clouds and using topic modelling for each cluster, to improve any outlier cluster gradings. Different clustering techniques can also be looked at.

There is a *tradeoff* here in the number of clusters vs. the human effort required. More are the number of cluster, better is the homogeneity of the data points, but so is an increased effort in grading the centroids of these clusters.




