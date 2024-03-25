import requests

session = requests.Session()

def login():
    url = ('http://127.0.0.1:8000/api/login/')
    data = {
        "username": "tej",
        "password": "123123"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(url, data=data, headers=headers)

    print(response.text)
    print(response.status_code)

def logout():
    url = ('http://127.0.0.1:8000/api/logout/')
    response = session.post(url)
    print(response.text)
    print(response.status_code)

login()
# logout()