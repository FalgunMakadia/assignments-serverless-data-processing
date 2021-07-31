import json
import boto3
import urllib
import csv
from botocore.errorfactory import ClientError
import re

TEST_VECTOR_CSV_FILE = "testVector.csv"
TRAIN_VECTOR_CSV_FILE = "trainVector.csv"

TEST_BUCKET_NAME = "testdatab00874635"
TRAIN_BUCKET_NAME = "traindatab00874635"

# https://gist.github.com/sebleier/554280
stop_word_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def create_s3_client():
	s3 = boto3.client('s3')
	return s3

# https://codereview.stackexchange.com/questions/217065/calculate-levenshtein-distance-between-two-strings-in-python
def lev_dist(word1, word2):
    if word1 == word2:
        return 0

    slen, tlen = len(word1), len(word2)
    dist = [[0 for i in range(tlen+1)] for x in range(slen+1)]
    for i in range(slen+1):
        dist[i][0] = i
    for j in range(tlen+1):
        dist[0][j] = j

    for i in range(slen):
        for j in range(tlen):
            cost = 0 if word1[i] == word2[j] else 1
            dist[i+1][j+1] = min(
                            dist[i][j+1] + 1,   
                            dist[i+1][j] + 1,   
                            dist[i][j] + cost   
                        )
    return dist[-1][-1]

def remove_stop_words(words_with_stop_words):
    # https://stackoverflow.com/questions/60702511
    # https://www.kite.com/python/answers/how-to-remove-stop-words-with-nltk-in-python
    words_without_stop_words = [word for word in word_list if not word.lower() in stop_words]
    return words_without_stop_words

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_filename = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    s3 = create_s3_client()
    s3_obj = s3.get_object(Bucket=bucket, Key=csv_filename)
    
    body_data = s3_obj["Body"].read().decode("utf-8")
    words_with_stop_words = re.findall(r"\w+", body_data, re.MULTILINE)
    words_without_stop_words = remove_stop_words(words_with_stop_words)
    
    try:

        if (csv_filename.startswith('3') or csv_filename.startswith('4')):
            csv_file_name = TEST_VECTOR_CSV_FILE
        else:            
            csv_file_name = TRAIN_VECTOR_CSV_FILE
        
        if (csv_filename.startswith('3') or csv_filename.startswith('4')):
            bucket_name = TEST_BUCKET_NAME
        else:
            bucket_name = TRAIN_BUCKET_NAME

        trainVector_obj = s3.get_object(Bucket=bucket_name, Key=csv_file_name)
        trainVector_body = bytearray(trainVector_obj["Body"].read())

    except s3.exceptions.NoSuchKey:
        print("Following file not found : " + csv_file_name)
        # https://www.programiz.com/python-programming/methods/built-in/bytearray
        trainVector_body = bytearray("current_word,next_word,levenshtein_distance\n", "utf-8")
        s3.put_object(Bucket=bucket_name, Key=csv_file_name, Body=trainVector_body)
    
    for i in range(len(words_without_stop_words)-1):
        first_word = words_without_stop_words[i]
        second_word = words_without_stop_words[i+1]

        lev_distance = lev_dist(first_word, second_word)
        
        trainVector_body.extend(bytes(f"{first_word},{second_word},{lev_distance}\n", "utf-8"))

    s3.put_object(Bucket=bucket_name, Key=csv_file_name, Body=trainVector_body)

