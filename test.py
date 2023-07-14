import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from collections import OrderedDict
import re
import requests
import time

app = Flask(__name__)

host = 'localhost'
port = 3306
user = 'root'
password = 'password'
database = 'frappe'

def get_mysql_connection():
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


connection = get_mysql_connection()
cursor = connection.cursor()

page = 196
base_url = "https://frappe.io/api/method/frappe-library"
while page<200:
	url = base_url + f"?page={page+1}"
	response = requests.get(url)
	print(response.status_code)
	response = response.json()
	# print(response)

	response = response['message']
	for i in response:
		# print(type(i['bookID']))

		# query_check_alreay_exits = "SELECT COUNT(*) FROM Library WHERE id = %s"
		# cursor.execute(query_check_alreay_exits, (i['bookID'],))
		# count = cursor.fetchone()[0]

		# if count>0:
		# 	continue

		new_book = (i['bookID'], i['title'], i['authors'], i['publisher'])
		query = "INSERT INTO Library (id, title, author, publisher) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, new_book)
		connection.commit()
	
	time.sleep(100)
	page+=1
	print("page no is ", page)

cursor.close()
connection.close()
