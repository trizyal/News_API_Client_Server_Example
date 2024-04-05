import requests
import json

class UserSession:
    def __init__(self):
        self.session = requests.Session()
        self.sessionURL = '127.0.0.1:8000'

s = UserSession()

def login(url, data):
    response = s.session.post("http://" + url + "/api/login", data=data)

    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        s.sessionURL = url

def logout():
    response = s.session.post("http://" + s.sessionURL+"/api/logout")
    print(response.text)
    print(response.status_code)

def post_story(payload):
    response = s.session.post("http://" + s.sessionURL + "/api/stories", data=payload)
    print(response.text)
    print(response.status_code)


def list_agencies():
    url = ('http://newssites.pythonanywhere.com/api/directory/')

    response = s.session.get(url)
    data = json.loads(response.text)

    return data

def get_news(url, payload):
    url = url + "/api/stories"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = s.session.get(url, params=payload, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        print("\n")
        for story in data["stories"]:
            print("Key".ljust(12)+ ":".ljust(5), story["key"])
            print("Headline".ljust(12) + ":".ljust(5) + story["headline"])
            print("Category".ljust(12) + ":".ljust(5) + story["story_cat"])
            print("Region".ljust(12) + ":".ljust(5) + story["story_region"])
            print("Author".ljust(12) + ":".ljust(5) + story["author"])
            print("Date".ljust(12) + ":".ljust(5) + story["story_date"])
            print("Details".ljust(12) + ":".ljust(5) + story["story_details"])
            print("\n")
    else:
        print("\n")
        print(response.status_code)
        print(response.text)
        print("\n")

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
                break
        print("\n")
        print("AGENCY: " + name)
        get_news(url, payload)
    else:
        data = list_agencies()
        count = 0
        for agency in data:
            count += 1

            url = agency["url"]
            name = agency["agency_name"]
            print("\n")
            print("AGENCY: " + name)
            get_news(url, payload)

            if count == 20:
                break


def delete_story(key):
    response = s.session.delete(s.sessionURL + "/api/stories" + key)
    print(response.text)
    print(response.status_code)


def client_welcome():
    title = '''
    \t\tooooo      ooo oooooooooooo oooooo   oooooo     oooo  .oooooo..o
    \t\t`888b.     `8' `888'     `8  `888.    `888.     .8'  d8P'    `Y8
    \t\t 8 `88b.    8   888           `888.   .8888.   .8'   Y88bo.
    \t\t 8   `88b.  8   888oooo8       `888  .8'`888. .8'     `"Y8888o.
    \t\t 8     `88b.8   888    "        `888.8'  `888.8'          `"Y88b
    \t\t 8       `888   888       o      `888'    `888'      oo     .d8P
    \t\to8o        `8  o888ooooood8       `8'      `8'       8""88888P'
            '''
    print("\n\n")
    print(title)
    print("\n\n\t\033[3mWelcome to the news client.\n")
    print("\tEnter a command to continue.")
    print("\tOr type \033[0m'help'\033[3m for a list of commands.\033[0m\n\n")

def print_client_options():
    print("\nOptions available:")
    print("\tlogin")
    print("\tlogout")
    print("\tpost")
    print("\tnews")
    print("\tlist")
    print("\tdelete")

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
        print("\n")
        for agency in data:
            print("Agency Name".ljust(15) + ":".ljust(5) + agency["agency_name"])
            print("Agency Code".ljust(15) + ":".ljust(5) + agency["agency_code"])
            print("URL".ljust(15) + ":".ljust(5) + agency["url"])
            print("\n")

    elif command == "delete":
        key = args[1]
        delete_story(key)

    elif command == "help":
        print_client_options()
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