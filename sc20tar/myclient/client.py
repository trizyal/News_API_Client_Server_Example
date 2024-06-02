import requests
import json

# Class to store the user session
class UserSession:
    def __init__(self):
        self.session = requests.Session()
        self.sessionURL = ''

# Session object
s = UserSession()


# Function to login to the server
# if the login is successful, the session URL is stored
def login(url, data):
    response = s.session.post("http://" + url + "/api/login", data=data)

    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        s.sessionURL = url


#  Function to logout from the url stored in the session
def logout():
    response = s.session.post("http://" + s.sessionURL+"/api/logout")
    print(response.text)
    print(response.status_code)


# Fuction to send a post request to the url stored in the session
def post_story(payload):
    response = s.session.post("http://" + s.sessionURL + "/api/stories", data=payload)
    print(response.text)
    print(response.status_code)


# Function to get the list of agencies from the directory
# The URL is hardcoded as it is not needed anywhere else in the code
# Returns the list of agencies, instead of printing it, as other functions might need it
def list_agencies():
    url = ('http://newssites.pythonanywhere.com/api/directory/')

    response = s.session.get(url)
    data = json.loads(response.text)

    return data


# ONE TIME FUNCTION TO REGISTER THE AGENCY
# This function is not needed for the client to work
# The client UI does not have access to this function
def register_agency():
    url = ('http://newssites.pythonanywhere.com/api/directory/')
    payload = {"agency_name": "Tejaswa Rizyal News Agency",
               "url": "http://sc20tar.pythonanywhere.com",
               "agency_code": "TAR02"}
    headers = {"Content-Type": "application/json"}

    data = json.dumps(payload)

    response = s.session.post(url, data=data, headers=headers)
    print(response.text)
    print(response.status_code)
#-----------------------------------------------------------


# Sends a payload to the URL provided
# If the response is successful, the news is printed
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


# Function to process the switches provided by the user
# By default, all switches are set to "*"
# If the user provides a switch, the value is updated
# Also calculates the URL and the name of the agency if -id is provided
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
        for agency in data: # loop through all agencies if -id is not provided
            count += 1

            url = agency["url"]
            name = agency["agency_name"]
            print("\n")
            print("AGENCY: " + name)
            get_news(url, payload) # requesting and printing handled by get_news function

            if count == 20: # limit the number of agencies to 20
                break


# Sends a delete request to the URL provided and attached the key to the URL
def delete_story(key):
    response = s.session.delete("http://" + s.sessionURL + "/api/stories/" + key)
    print(response.text)
    print(response.status_code)


# Just Visuals
# Prints the welcome message
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


# Prints the options available to the user
def print_client_options():
    print("\nOptions available:")
    print("\tlogin")
    print("\tlogout")
    print("\tpost")
    print("\tnews")
    print("\tlist")
    print("\tdelete")
    print("\n\tYou can also type '<command> -help' for more information on a command.\n")



# Parses user input
# Calls the appropriate function
# Commands that require arguments are handled here
# Also allows -help to be used with commands
# which will print the usage of the command
def process_input(command, args):

    if command == "login":

        if len(args) < 2 or args[1] == "-help":
            print("Usage: login <url>\n")
            return

        # User Prompts
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(args[1], {"username": username, "password": password})

    elif command == "logout":

        if len(args) > 1:
            print("Usage: logout")
            print("No arguments required.\n")
            return
        if s.sessionURL == '':
            print("You are not logged in.\n")
            return

        logout()

    elif command == "post":

        if len(args) > 1:
            print("Usage: post")
            print("Enter the headline, category, region and details when prompted.\n")
            return

        # User Prompts
        headline = input("Enter headline: ")
        category = input("Enter category: ")
        region = input("Enter region: ")
        details = input("Enter details: ")
        payload = {"headline": headline, "category": category, "region": region, "details": details}

        post_story(json.dumps(payload))

    elif command == "news":

        if len(args) > 1 and args[1] == "-help":
            print("Usage: news [-id=<agency_code>] [-cat=<category>] [-reg=<region>] [-date=<date>]")
            print("All switches are optional.")
            print("If -id is not provided, news from 20 random agencies will be displayed.\n")
            return

        process_news_switches(args)

    elif command == "list":

        if len(args) > 1:
            print("Usage: list")
            print("No arguments required.\n")
            return

        data = list_agencies()

        # Printing is handled here as the code is not too long
        print("\n")
        for agency in data:
            print("Agency Name".ljust(15) + ":".ljust(5) + agency["agency_name"])
            print("Agency Code".ljust(15) + ":".ljust(5) + agency["agency_code"])
            print("URL".ljust(15) + ":".ljust(5) + agency["url"])
            print("\n")

    elif command == "delete":

        if len(args) < 2 or args[1] == "-help":
            print("Usage: delete <key>\n")
            return
        if s.sessionURL == '':
            print("You are not logged in.\n")
            return

        key = args[1]
        delete_story(key)

    elif command == "help":
        print_client_options()

    # ONE TIME FUNCTION TO REGISTER THE AGENCY - NOT NEEDED FOR CLIENT
    # elif command == "register":
        # register_agency()

    else:
        print("Invalid command. Type 'help' for a list of commands.\n")

def main():
    client_welcome()
    user_input = input(">>> ")
    while user_input != "exit": # infinite loop until user types 'exit'
        user_input = user_input.split()
        command = user_input[0] # first word is the command, so separating it is beneficial
        process_input(command, user_input) # command and arguments can be dealt with separately
        user_input = input(">>> ")


if __name__ == '__main__':
    main()