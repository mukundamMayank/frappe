# import requests
# import json


# title = None
# authors = None


# response = requests.get('https://frappe.io/api/method/frappe-library?publisher=University Of Chicago Press&page=12').content.decode('utf-8')
# response_json = json.loads(response)
# print(response_json)

import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from collections import OrderedDict
import re
import requests
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

# # @app.route('storeBooks', methods=['POST'])
# def helper(request):

# 	data = request.get_json()

# 	# if len(data) == 0:
# 	# 	return jsonify({'message': 'Need to make atleast one entry field'})

# 	base_url = "https://frappe.io/api/method/frappe-library"

# 	query_params = ""
# 	if 'title' in data:
# 		if len(query_params) == 0:
# 			query_params+="?"+"title="+data.get('title')
# 		else:
# 			query_params+="&"+"title="+data.get('title')

# 	if 'authors' in data:
# 		if len(query_params) == 0:
# 			query_params+="?"+"authors="+data.get('authors')
# 		else:
# 			query_params+="&"+"authors="+data.get('authors')

# 	if 'publisher' in data:
# 		if len(query_params) == 0:
# 			query_params+="?"+"publisher="+data.get('publisher')
# 		else:
# 			query_params+="&"+"publisher="+data.get('publisher')

# 	url = base_url + query_params
# 	# print(url)

# 	page = 1
# 	last_page = None
# 	books = []
# 	while last_page is None or page<=last_page:
# 		final_url = url + f"&page={page}"
# 		response = requests.get(final_url)
# 		print(final_url, ' ', response.status_code)
# 		if response.status_code == 200:
# 			# print(response.json())
# 			books.append(response.json())

# 			link_header = response.headers.get('Link', '')
# 			last_page_match = re.search(r'&page=(\d+)>; rel="last"', link_header)

# 			print(page, ' ', last_page)

# 			if last_page_match:
# 				last_page = int(last_page_match.group(1))

# 			page += 1
# 		else:
# 			page += 1

# 	return books



@app.route('/storeBooks', methods=['POST'])
def storeBooks():
	data  = request.get_json()
	query = None
	params = None
	total_required_books = 0
	print(data)

	if 'requirement' in data:
		total_required_books = data['requirement']

	if 'title' in data and data['title']!='':
		if query is None:
			query = "Select id, title, author, publisher from Library where title = %s"
			params = (data['title'], )
		else:
			query+="AND title = %s"
			params+= (data['title'])

	if 'publisher' in data and data['publisher']!='':
		if query is None:
			query = "Select id, title, author, publisher from Library where publisher = %s or publisher like %s"
			params= (data['publisher'],f"%{data['publisher']}%", )
		else:
			query+="AND (publisher = %s or publisher LIKE %s)"
			params+= (data['publisher'],f"%{data['publisher']}%", )

	if 'author' in data and data['author']!='':
		if query is None:
			query = "Select id, title, author, publisher from Library where author = %s or author like %s"
			params = (data['author'], f"%{data['author']}%", )
		else:
			query+="AND (author = %s or author like %s)"
			params+= (data['author'], f"%{data['author']}%", )

	print(query, ' ', params)
	cursor.execute(query, params)
	cnt = 0

	rows = cursor.fetchall()
	# print(rows)
	for i in rows:
		if int(total_required_books) != 0:
			if cnt == int(total_required_books):
				continue

		query_check = "Select COUNT(*) from Books where id = %s"
		params_check = (i[0],)
		cursor.execute(query_check, params_check)
		count = cursor.fetchone()[0]
		cnt+=1

		if count>0:
			#update stocks+1
			temp_query = "Select stocks from Books where id = %s"
			temp_params = (i[0], )
			cursor.execute(temp_query, temp_params)

			temp_query_2 = "update Books set stocks = %s where id = %s"
			temp_params_2 = (cursor.fetchone()[0]+1, i[0])
			cursor.execute(temp_query_2, temp_params_2)
			connection.commit() 



		else:
			insert_query = "INSERT INTO Books (id, title, author, publisher, stocks) VALUES (%s, %s, %s, %s, %s)"
			insert_params = (i[0], i[1], i[2], i[3], 1)
			cursor.execute(insert_query, insert_params)
			connection.commit()

	# cursor.close()
	# connection.close()


			# cursor.execute(query, params)
			# print(cursor.fetchone())


	return {'message':'added successfully'}


@app.route('/getBooks', methods = ['GET'])
def getBooks():
	data = request.args
	# print(request.args)

	query = None
	params = None
	if 'title' in data and data.get('title') != '':
		if query is None:
			query = "Select * from Books where title = %s"
			params = (data.get('title'), )
		else:
			query+= " and title = %s"
			params+= (data.get('title'), )

	if 'author' in data and data.get('author') != '':
		if query is None:
			query = "Select * from Books where author = %s or author like %s"
			params = (data.get('author'), f"%{data.get('author')}%",)
		else:
			query+="AND (author = %s or author like %s)"
			params+= (data.get('author'), f"%{data.get('author')}%", )


	print(query, params)
	cursor.execute(query , params)

	return {'res': cursor.fetchall()}

	# if len(data) == 0:
	# 	query = "Select * from Books"
	# 	cursor.execute(query)
	# 	return {'res': cursor.fetchall()}
	# else:
	# 	query = None
	# 	params = None
	# 	if 'title' in data and data.get('title') != '':
	# 		if query is None:
	# 			query = "Select * from Books where title = %s"
	# 			params = (data.get('title'), )
	# 		else:
	# 			query+= " and title = %s"
	# 			params+= (data.get('title'), )

	# 	if 'author' in data and data.get('author') != '':
	# 		if query is None:
	# 			query = "Select * from Books where author = %s or author like %s"
	# 			params = (data.get('author'), f"%{data.get('author')}%",)
	# 		else:
	# 			query+="AND (author = %s or author like %s)"
	# 			params+= (data.get('author'), f"%{data.get('author')}%", )

	# 	print(query, params)
	# 	cursor.execute(query , params)
	# 	return {'res': cursor.fetchall()}


@app.route('/registerMembers', methods = ['POST'])
def registerMembers():
	data = request.get_json()
	email = None
	if 'email' in data:
		email = data['email']
	else:
		return {'res': 'Please fill the email'}

	query = "Select count(*) from Members where email = %s"
	params = (email, )

	cursor.execute(query, params)
	count = cursor.fetchone()[0]

	if count>0:
		return {'res':'This email is already registered'}
	else:
		query = "INSERT INTO Members (email, outstanding_fee) VALUES (%s, %s)"
		params = (email, 0)
		cursor.execute(query, params)
		connection.commit()

		# cursor.close()
		# connection.close()
		return {'res': 'Member successfully registered'}


@app.route('/issueBooks', methods = ['POST'])
def issueBooks():
	data = request.get_json()
	print(data)
	email = None
	title = None
	if 'issue_email' not in data or 'title' not in data:
		return {'res': 'Please fill the email & title of the book to be issued'}
	else:
		email = data['issue_email']
		title = data['title']

	query = "Select count(*) from Members where email = %s"
	params = (email, )

	cursor.execute(query, params)
	count = cursor.fetchone()[0]

	title_check_query = "Select count(*) from Books where title = %s"
	params_title_check = (title, )

	cursor.execute(title_check_query, params_title_check)
	count2 = cursor.fetchone()[0]

	print(count2, ' ', title)
	print(count, ' ', email)

	if count>0 and count2>0:
		query = "SELECT id, outstanding_fee FROM Members WHERE email = %s"
		params = (email,)
		cursor.execute(query, params)
		temp = cursor.fetchone()
		existing_books = temp[0]
		outstanding_fee = temp[1]

		if outstanding_fee > 500:
			return {'res':'The book cannot be issued as it has crossed the limits'}

		book_id_query = "Select id, stocks from Books where title = %s"
		params = (data['title'], )
		cursor.execute(book_id_query, params)
		curr_book_stock = cursor.fetchone()
		new_bookID = curr_book_stock[0]
		stocks = curr_book_stock[1]

		if stocks == 0:
			return {'res': 'There are no books left with the title you are searching for'}

		if existing_books is None:
			updated_books = new_bookID
		else:
			updated_books = existing_books + ',' + new_bookID
		update_query = "UPDATE Members SET id = %s, outstanding_fee = %s, issued_at = %s WHERE email = %s"
		update_params = (updated_books, outstanding_fee+100, datetime.now(), email)
		cursor.execute(update_query, update_params)

		update_book_query = "UPDATE Books SET stocks = %s WHERE id = %s"
		update_books_params = (stocks-1, new_bookID, )
		cursor.execute(update_book_query, update_books_params)

		connection.commit()

		# cursor.close()
		# connection.close()

		return {'res': 'book issued successfully'}


	else:
		return {'res': 'Email id not registered or book with mentioned title not present'}



@app.route("/returnBook", methods = ['POST'])
def returnBook():
	data = request.get_json()
	print(data)
	if 'return_book_title' not in data:
		return {'res': 'Please add the title of the book you want to return'}

	title = data['return_book_title']
	email = data['return_member_email']

	book_id_query = "Select id, stocks from Books where title = %s"
	book_id_params = (title, )

	connection = get_mysql_connection()
	cursor = connection.cursor()

	cursor.execute(book_id_query, book_id_params)

	temp = cursor.fetchone()

	book_id = temp[0]
	stocks = temp[1]

	member_to_book_query = "Select id, outstanding_fee from Members where email = %s"
	member_to_book_params = (email, )
	cursor.execute(member_to_book_query, member_to_book_params)

	temp = cursor.fetchone()
	books_id = temp[0]
	outstanding_fee = temp[1]

	if book_id not in books_id:
		return jsonify({'res': 'You have not issued this book'})


	update_book_stock_query = "update Books set stocks = %s where id = %s"
	update_book_stock_params = (stocks+1, books_id, )
	cursor.execute(update_book_stock_query, update_book_stock_params)
	connection.commit()

	connection = get_mysql_connection()
	cursor = connection.cursor()

	print(stocks, ' ', update_book_stock_query, ' ', update_book_stock_params)

	books_list = books_id.split(',')
	books_list = [curr_book_id for curr_book_id in books_list if curr_book_id != str(book_id)]
	updated_books = ','.join(books_list)

	update_query = "UPDATE Members SET id = %s, outstanding_fee = %s WHERE email = %s"
	update_params = (updated_books, outstanding_fee-80, email)
	cursor.execute(update_query, update_params)
	connection.commit()

	# cursor.close()
	# connection.close()

	return jsonify({'res': 'book return successfully done'})


@app.route("/getAllUsers", methods=['GET'])
def getAllUsers():
	query = "Select * from Members"
	cursor.execute(query)
	return {'res': cursor.fetchall()}

@app.route("/deleteMember", methods=['DELETE'])
def deleteMembers():
	data = request.get_json()
	email = data['delete_member_email']

	books_id_query = "Select id from Members where email=%s"
	books_id_params = (email, )
	# connection = get_mysql_connection()
	# cursor = connection.cursor()

	cursor.execute(books_id_query, books_id_params)

	temp = cursor.fetchone()
	print(temp)

	if temp:

		books_id = temp[0]
		books_list = books_id.split(',')
		for i in books_list:
			if i == '':
				continue
			get_stock_query = "Select stocks from Books where id = %s"
			get_stock_params = (i, )
			cursor.execute(get_stock_query, get_stock_params)
			stocks = cursor.fetchone()[0]

			update_stock_query = "update Books set stocks = %s where id = %s"
			update_stock_params = (stocks+1, i, )
			cursor.execute(update_stock_query, update_stock_params)
			connection.commit()

	query = "DELETE from Members where email=%s"
	params = (email, )
	cursor.execute(query, params)
	connection.commit()


	# cursor.close()
	# connection.close()

	return {'res':'Member deleted successfully'}

@app.route("/deleteBook", methods=['DELETE'])
def deleteBook():
	data = request.get_json()
	title = data['delete_book_title']
	query = "DELETE from Books where title = %s"
	params = (title, )
	cursor.execute(query, params)
	connection.commit()

	# cursor.close()
	# connection.close()

	return {'res':'Book deleted successfully'}

if __name__ == '__main__':
    app.run(port = 8000)


	# response = requests.get(base_url + query_params).content.decode('utf-8')
	# response_json = json.loads(response)
	# books = response_json['message']

	# for i in books:
	# 	new_book = (i['bookID'], i['title'], i['authors'], i['publisher'], )


# import requests
# import re

# def get_books_by_title(title):
#     books = []
#     page = 1
#     last_page = None
#     while last_page is None or page <= last_page:
#         url = f'https://frappe.io/api/method/frappe-library?page={page}'
#         response = requests.get(url)
#         # print(response.content)
        
#         if response.status_code == 200:
#             # books += response.json()
            
#             # Extract last page from Link header

#             link_header = response.headers.get('Link', '')
#             last_page_match = re.search(r'&page=(\d+)>; rel="last"', link_header)
            
#             if last_page_match:
#                 last_page = int(last_page_match.group(1))
                
#             page += 1
#             # print(last_page, ' ', page)
#         else:
#             break
#     print(page)
    # return books


# title = "The Poetry of Sylvia Plath"
# get_books_by_title(title)



