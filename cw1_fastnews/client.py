import requests
import json

class UserSession:
    def __init__(self):
        self.session = requests.Session()
        self.sessionURL = '127.0.0.1:8000'

s = UserSession()

def login(url, data):
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = s.session.post("http://" + url + "/api/login", data=data)

    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        s.sessionURL = url

def default_login():
    url = ('http://127.0.0.1:8000/api/login')
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
    response = s.session.post("http://" + s.sessionURL+"/api/logout")
    print(response.text)
    print(response.status_code)

def post_story(payload):
    response = s.session.post("http://" + s.sessionURL + "/api/stories", data=payload)
    print(response.text)
    print(response.status_code)

# def post_test():
#     url = ('http://127.0.0.1:8000/api/stories/')
#     payload = {
#         "headline": "Test headline",
#         "category": "pol",
#         "region": "uk",
#         "details": "Test details"
#     }
#     payload = json.dumps(payload)
#     response = s.session.post(url, data=payload)
#     print(response.text)
#     print(response.status_code)

def list_agencies():
    url = ('http://newssites.pythonanywhere.com/api/directory/')
    response = s.session.get(url)
    data = json.loads(response.text)

    return data

def get_news(url, payload):
    url = url + "/api/stories"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = s.session.get(url, params=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)
        print("\n")
        for story in data["stories"]:
            print("Key: ".ljust(15), story["key"])
            print("Headline: ".ljust(15) + story["headline"])
            print("Category: ".ljust(15) + story["story_cat"])
            print("Region: ".ljust(15) + story["story_region"])
            print("Author: ".ljust(15) + story["author"])
            print("Date: ".ljust(15) + story["story_date"])
            print("Details: ".ljust(15) + story["story_details"])
            print("\n")
    else:
        print(response.text)

def process_news_switches(data):
    id = "*"
    cat = "*"
    reg = "*"
    date = "*"
    for switch in data:
        if switch.startswith("-id="):
            id = switch.split("=")[1][1:-1] # remove quotes from string
        elif switch.startswith("-cat="):
            cat = switch.split("=")[1][1:-1] # remove quotes from string
        elif switch.startswith("-reg="):
            reg = switch.split("=")[1][1:-1] # remove quotes from string
        elif switch.startswith("-date="):
            date = switch.split("=")[1][1:-1] # remove quotes from string
    payload = {"story_cat": cat, "story_region": reg, "story_date": date}

    if id != "*":
        data = list_agencies()
        for agency in data:
            if agency["agency_code"] == id:
                url = agency["url"]
                name = agency["agency_name"]
                print(name)
                print(url)
                break
        print("AGENCY: " + name)
        get_news(url, payload)


def delete_story(key):
    response = s.session.delete(s.sessionURL + "/api/stories" + key)
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
        process_news_switches(args)

    elif command == "list":
        data = list_agencies()
        for agency in data:
            print(json.dumps(agency, indent=4))

    elif command == "delete":
        key = args[1]
        delete_story(key)

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