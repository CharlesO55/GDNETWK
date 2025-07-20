# WikiLinks Python Game
Wikilinks is a game oriented at entirely navigating Wikipedia through its articles' hyperlinks.

For example, when tasked with finding Shinzo Abe, one may take the following route Cats > Animals > Capybarra > Japan > Japanese politics > Shinzo Abe.

[Watch Longplay](https://youtu.be/CwZ5zJsZbCA)

# Game Mechanics
1. Player is instructed by Server to search for an item within a time limit.
2. When timer finishes, Client app will take a screenshot of the current screen.
3. Wait for server to give a score on the article/image found.
4. Repeat  

# Server
Contains an `Ollama` model for image recognition of submitted screeenshots.

Responsible for sending search instructions and grading results for any number of Clients. 

# Client
Responsible for first connecting to Server.

This is a simple tkinter UI app with Selenium opening a random Wikipedia page start.

When timer finishes, take a screenshot and send to Server.
