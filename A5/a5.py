import boto3
import random
import string
import time

aws_access_key_id="ASIA5KWEVBPZTBV757XT"
aws_secret_access_key="6NCytVsnuTGiKifvCJGN7DSs2j3oPouQYdglxUtM"
aws_session_token="FwoGZXIvYXdzEJ7//////////wEaDA/N/Rehoha62kfNtyK/AQmsvuUdXRPW8AbzMTstZL9VuywK22yG+HYDKqmABKdAP/+ol47G+gX/+3pbuFq7Aw5v3wWtJ3cAnDcx2oOq3pzsa1pDqAxfXKI3LLn/EK+fQiZgl22OISs3iWqVXGIDQO+DuJ8zBiCrubY2IXeQVNLNVTMyIjjU6E5AWw/ec3Fylna+Zus+FMmESNfiN/eWREMxQPxFcEPwyTpn3M17QNgsiuYOddOAtUjwyXIpuJE0HA0AaWgA0FjNYKvLJx17KKSsjIgGMi3/lfEfCRdHZ4OOr7GRdaRBUbGvtVXo1Y2R4ni4EF7SdY3M01B/Z3WyrATw3Xc="
aws_sqs_queue_name="HalifaxFlowersSQS"

def get_queue():
	resource = boto3.resource('sqs', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)	
	queue = resource.get_queue_by_name(QueueName=aws_sqs_queue_name)
	return queue

def send_message_to_user(msg):
	queue = get_queue()
	response = queue.send_message(MessageBody=msg)
	return response

def prepare_bouquet_order_data():
	letters = string.ascii_uppercase
	order_id = ''.join(random.choice(letters) for i in range(8))
	flower_list = ['Rose', 'Lily', 'Tulip', 'Orchid', 'Daisy']
	flower_count_in_order = random.randrange(len(flower_list))
	selected_flowers_in_order = random.sample(flower_list, flower_count_in_order)
	each_flower_count_in_order = random.sample(range(1, 10), len(selected_flowers_in_order))
	return order_id, selected_flowers_in_order, each_flower_count_in_order


def prepared_order():
	order_id, selected_flowers_in_order, each_flower_count_in_order = prepare_bouquet_order_data()

	if(len(selected_flowers_in_order) == 0):
		order_id, selected_flowers_in_order, each_flower_count_in_order = prepare_bouquet_order_data()

	msg_content = "Hey Alice, a new Order is here! \n\nOrder ID: "+ str(order_id) +"\n\nOrder Content \n============\n"

	for i in range(len(selected_flowers_in_order)):
		msg_content = msg_content + (selected_flowers_in_order[i] + ' --> ' + str(each_flower_count_in_order[i]) + '\n')

	return msg_content


def run():

	count = 0

	while True:

		message_content = prepared_order()
		print(message_content)

		count += 1

		response = send_message_to_user(message_content + '\n\n['+str(count)+' order(s) so far!]')
		print(response)

		print('\nWaiting for next order...\n')
		time.sleep(300)

run()