import requests
import json


# title = None
# authors = None
# json_data = {}

# json_data['email'] = "mayank.7967@gmail.com"
# json_data['title'] = "Mortals"


# # response = requests.post('http://localhost:8000/storeBooks', json = json_data).content
# # # response_json = json.loads(response)
# # print(response)

# response = requests.get('http://localhost:8000/getBooks?author=Rumi').content.decode('utf-8')

# # response = requests.post('http://localhost:8000/returnBook', json=json_data).content
# print(response)


option = int(input('Enter a number\n 1. To store Books\n 2.Get Books by author & title\n 3. Register new Members\n 4. Issue Books\n 5. Return Book\n 6. Check Members\n 7. Delete Members\n 8. Delete Books\n'))


if option == 1:
	json_data = {}
	json_data['title'] = None
	json_data['publisher'] = None
	json_data['author'] = "Rumi"
	json_data['requirement'] = 2

	response = requests.post('http://localhost:8000/storeBooks', json = json_data).content
	# print(response)
	# response = json.loads(response)
	print(response)

elif option == 2:
	title = "The Eden Express: A Memoir of Insanity"
	author = None

	response = requests.get(f'http://localhost:8000/getBooks?title={title}&author={author}').content.decode('utf-8')
	print(response)

elif option == 3:
	json_data = {}
	json_data['email'] = 'mayank.7967@gmail.com'

	response = requests.post('http://localhost:8000/registerMembers', json = json_data).content
	response = json.loads(response)
	print(response)

elif option == 4:
	json_data = {}
	json_data['issue_email'] = 'mayank.7967@gmail.com'
	json_data['title'] = 'The Eden Express: A Memoir of Insanity'

	response = requests.post('http://localhost:8000/issueBooks', json = json_data).content
	response = json.loads(response)
	print(response)

elif option == 5:
	json_data = {}
	json_data['return_book_title'] = "The Eden Express: A Memoir of Insanity"
	json_data['return_member_email'] = 'mayank.7967@gmail.com'

	response = requests.post('http://localhost:8000/returnBook', json = json_data).content
	response = json.loads(response)
	print(response)

elif option == 6:
	response = requests.get('http://localhost:8000/getAllUsers').content.decode('utf-8')
	print(response)

elif option == 7:
	json_data = {}
	json_data['delete_member_email'] = 'mayank.79671@gmail.com'

	response = requests.delete('http://localhost:8000/deleteMember', json = json_data).content
	response = json.loads(response)
	print(response)

elif option == 8:
	json_data = {}
	json_data['delete_book_title'] = "The Eden Express: A Memoir of Insanity"

	response = requests.delete('http://localhost:8000/deleteBook', json = json_data).content
	response = json.loads(response)
	print(response)


