import os
import csv
import io
import boto3

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
final_words = []
current_record = []
lev_distance = 0
BUCKET_FOR_CSV_FILE = 'sampledatab00874635'
CSV_FILE_NAME_ON_BUCKET = 'trainVector.csv'

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

def create_csv_writer():
	csvio = io.StringIO()
	writer = csv.writer(csvio)
	return csvio, writer

def create_s3_client():
	s3 = boto3.client('s3')
	return s3


def final_words_after_removing_stop_words():
	words = []
	path = 'Dataset/Train/'
	dirr = os.fsencode(path)

	for file in os.listdir(dirr):
		fileName = os.fsdecode(file)

		with open(path+fileName,'r') as file:
			for line in file:
				for word in line.split():
					if word.lower() in stop_words:
						pass
					else:
						words.append(word)

	return words


csvio, writer = create_csv_writer()
writer.writerow(['Current_Word', 'Next_Word', 'Levenshtein_distance'])


def write_data_in_csv_file():

	final_words = final_words_after_removing_stop_words()

	for i in range(len(final_words)):
		try:
			lev_distance = lev_dist(final_words[i], final_words[i+1])

			current_record.extend([final_words[i], final_words[i+1], lev_distance])

			writer.writerow(current_record)

			current_record.clear()

		except Exception as e:
			print("EOF occurred or Error: " + str(e))


def put_object_on_bucket(bucket_name, csv_file_name):

	write_data_in_csv_file()

	try:
		s3client = create_s3_client()
		s3client.put_object(Body=csvio.getvalue(), ContentType='text/csv', Bucket = bucket_name, Key = csv_file_name)
		print("CSV File '" + csv_file_name + "' is Successfully Uploaded on '" + bucket_name + "' bucket!")

	except Exception as e:
		print("Error occurred while uploading CSV file to " + bucket_name + " Bucket!")
		print(e)


put_object_on_bucket(BUCKET_FOR_CSV_FILE, CSV_FILE_NAME_ON_BUCKET)