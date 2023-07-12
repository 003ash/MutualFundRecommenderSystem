# MutualFundRecommenderSystem

##### Website: https://mutual-fund-recommender-system.onrender.com

### Description:

This repository hosts a Mutual Fund Recommender System built using clustering algorithms. The recommender system leverages the power of machine learning and data analysis techniques to provide personalized investment recommendations for mutual fund investors.

The system utilizes clustering algorithms, such as K-means, hierarchical clustering, DBSCAN, and Agglomerative to group mutual funds based on various features, such as historical performance, risk profile, expense ratio, etc. These clustering algorithms help identify similar groups of mutual funds, allowing the system to make informed recommendations based on a user's investment preferences.

##### Metrics used

1. **Silhouette score**:
The Silhouette Score is a metric used to evaluate the quality of clustering results. It provides a measure of how well instances (data points) within a cluster are separated from instances in other clusters. The Silhouette Score ranges from -1 to 1, where a higher score indicates better clustering performance:
A score close to 1 suggests that instances within a cluster are well-separated from instances in other clusters. This indicates a good clustering structure. A score close to 0 indicates that instances are on or very close to the decision boundary between two neighboring clusters. This suggests overlapping or ambiguous clusters.
A score close to -1 indicates that instances might have been assigned to the wrong clusters.

2. **Inertia**:
Inertia is a metric used to assess the quality of clustering algorithms, such as K-means. It quantifies the sum of squared distances between data points and the centroids of their assigned clusters. Minimizing inertia is the objective of clustering, as lower inertia indicates more compact and homogeneous clusters.

##### Reference paper

Clustering Models for mutual fund recommender system: https://www.irjet.net/archives/V10/i4/IRJET-V10I463.pdf


