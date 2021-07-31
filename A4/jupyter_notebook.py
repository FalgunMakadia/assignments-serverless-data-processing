# In [1]

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas
import boto3
import io


# In [2]
s3_client = boto3.client("s3")


# In [3]
TRAINING_DATA_BUCKET_NAME = 'traindatab00874635'
TEST_DATA_BUCKET_NAME = 'testdatab00874635'


# In [4]
TRAIN_VECTOR_CSV_FILE = 'trainVector.csv'
TEST_VECTOR_CSV_FILE = 'testVector.csv'


# In [5]
training_data_obj = s3_client.get_object(Bucket=TRAINING_DATA_BUCKET_NAME, Key=TRAIN_VECTOR_CSV_FILE)
training_data_obj


# In [6]
training_data_frame = pandas.read_csv(io.BytesIO(training_data_obj["Body"].read()))
training_data_frame


# https://stackoverflow.com/questions/25757042
# In [7]
training_data_frame["current_word"] = training_data_frame["current_word"].apply(lambda x: hash(x))


# https://stackoverflow.com/questions/25757042
# In [8]
training_data_frame["next_word"] = training_data_frame["next_word"].apply(lambda x: hash(x))


# https://www.geeksforgeeks.org/python-pandas-series-to_numpy/
# In [9]
training_df_to_np = training_data_frame.to_numpy()
print(training_df_to_np)


# In [10]
print(type(training_df_to_np))


# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# In [11]
k_means_op = KMeans(n_clusters=7, random_state=0).fit(training_df_to_np)
print(k_means_op)


# In [12]
print(type(k_means_op))


# In [13]
k_means_op.labels_


# In [14]
print(type(k_means_op.labels_))


# In [15]
test_data_obj = s3_client.get_object(Bucket=TEST_DATA_BUCKET_NAME, Key=TEST_VECTOR_CSV_FILE)
test_data_obj


# In [16]
test_data_frame = pandas.read_csv(io.BytesIO(test_data_obj["Body"].read()))
test_data_frame


# In [17]
test_data_frame["current_word"] = test_data_frame["current_word"].apply(lambda x: hash(x))


# In [18]
test_data_frame["next_word"] = test_data_frame["next_word"].apply(lambda x: hash(x))


# In [19]
test_df_to_np = test_data_frame.to_numpy()
print(test_df_to_np)


# In [20]
print(type(test_df_to_np))


# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# In [21]
k_means_op.predict(test_df_to_np)


# In [22]
print(type(k_means_op.cluster_centers_))
