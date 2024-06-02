The client app for news api. Coursework 1.

URL: sc20tar.pythonanywhere.com

Module Leader's Admin and Author account-
USERNAME: ammar
PASSWORD: asdf@1234

Intructions for the client app-
The client CLI provides the following commands:

help-
syntax: help
    This command gives the user a list of all the available commands.

login-
syntax: login <url>
    This command allows the user to log into a news service.
    The client app promts the user to enter their username and password
    once the command is entered.

logout-
syntax: logout
    This will log the user out from the current session.

post-
syntax: post
    This command allows the user to post a news story to the news agency they are loggen into.
    Once the command is typed, the application prompts the user to enter the headline, category
    region and details one by one.
    The user has to be logged in to an agency to post newws stories.

news-
syntax: news [-id="<id>"] [-cat="<cat>"] [-reg="<reg>"] [-date="<date>"]
    This command allows the user to request news from different agencies.
    the -id, -cat, -reg, and -date are all optional switches that allow the user to request
    filtered news.
    In case the -id (News Agnecy ID) switch is left, the alint will aggregate news from 20 random news agencies,
    and display them one by one, with the agency name before a list of the news stories the
    agency returned.
    The -date switch should be entered in the "dd/mm/yyyy" format.
    The -cat (category) switch can be one of the following: tech, pol, art, trivia.
    The -reg (region) switch can be one of the following: uk, eu, w

list-
syntax: list
    This command lists all the news services that are registers to the directory.

delete-
syntax: delete <story_key>
    This command allows the user to send a delete request for the story with key <story_key>.
    The user must be logged in to use this command and must be the author of the story to delete it.

exit-
syntax: exit
    This command exits the client application.

Other Instruction:
- Do NOT include "http://" when entering the URL for a service.
- You can also type <command> -help to view its syntax and use.