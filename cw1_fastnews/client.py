import requests
import json

class UserSession:
    def __init__(self):
        self.session = requests.Session()
        self.sessionURL = 'http://127.0.0.1:8000'

s = UserSession()

def login(url, data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = s.session.post(url + "/api/login/", data=data, headers=headers)

    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        s.sessionURL = url

def default_login():
    url = ('http://127.0.0.1:8000/api/login/')
    data = {
        "username": "tej",
        "password": "Qwerty@123"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = s.session.post(url, data=data, headers=headers)

    print(response.text)
    print(response.status_code)

def logout():
    # url = ('http://127.0.0.1:8000')
    response = s.session.post(s.sessionURL+"/api/logout/")
    print(response.text)
    print(response.status_code)

def post_story(payload):
    headers = {"Content-Type": "application/json"}
    # payload = json.dumps(payload)
    response = s.session.post(s.sessionURL + "/api/stories/", data=payload, headers=headers)
    print(response.text)
    print(response.status_code)

def post_test():
    url = ('http://127.0.0.1:8000/api/stories/')
    payload = {
        "headline": "Test headline",
        "category": "pol",
        "region": "uk",
        "details": "Test details"
    }
    payload = json.dumps(payload)
    response = s.session.post(url, data=payload)
    print(response.text)
    print(response.status_code)

def get_news():
    url = ('http://127.0.0.1:8000/api/stories/')
    payload = {
        "story_cat": "tech",
        "story_region": "uk",
        "story_date": "2024-03-27"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = s.session.get(url, data=payload, headers=headers)
    # r = json.loads(response.text)
    # print(r)
    print(response.text)
    print(response.status_code)

def client_welcome():
    title = '''
    ooooo      ooo oooooooooooo oooooo   oooooo     oooo  .oooooo..o
    `888b.     `8' `888'     `8  `888.    `888.     .8'  d8P'    `Y8
     8 `88b.    8   888           `888.   .8888.   .8'   Y88bo.
     8   `88b.  8   888oooo8       `888  .8'`888. .8'     `"Y8888o.
     8     `88b.8   888    "        `888.8'  `888.8'          `"Y88b
     8       `888   888       o      `888'    `888'      oo     .d8P
    o8o        `8  o888ooooood8       `8'      `8'       8""88888P'
            '''

    print(title)
    print("\n\n\tWelcome to the news client.")
    print("\n\t\tEnter a command to continue.")
    print("\t\tOr type 'help' for a list of commands.")

def print_client_options():
    print("\n\tOptions available:")
    print("\t\t login")
    print("\t\t logout")
    print("\t\t post")
    print("\t\t news")
    print("\t\t list")
    print("\t\t delete")

def process_input(command, args):

    if command == "login":
        if args[1] == "-help":
            print("Usage: login <url>")
            return
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(args[1], {"username": username, "password": password})

    elif command == "logout":
        logout()

    elif command == "post":
        headline = input("Enter headline: ")
        category = input("Enter category: ")
        region = input("Enter region: ")
        details = input("Enter details: ")
        payload = {"headline": headline, "category": category, "region": region, "details": details}
        post_story(json.dumps(payload))

    elif command == "news":
        get_news()

    elif command == "list":
        pass
    elif command == "delete":
        pass
    elif command == "help":
        print_client_options()
    elif command == "test":
        default_login()
    else:
        print("Invalid command. Type 'help' for a list of commands.")

def main():
    client_welcome()
    user_input = input(">>> ")
    while user_input != "exit":
        user_input = user_input.split()
        command = user_input[0]
        process_input(command, user_input)
        user_input = input(">>> ")


if __name__ == '__main__':
    main()