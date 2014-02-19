REST API
========

Goals: Write a REST API that will maintain a list of words, and display them through the desired paths 

# Assumptions:

* State will not be maintained: once the server is restarted the word list will go away
* Data is sent in JSON format over HTTP: only GET and PUT are exposed at their respective landing spots
* Data must be updated on the web page automatically
* Errors must be handled well

# Steps to test and verify:

* Create a python virtual environment (I used virtualenvwrapper), and install the packages according to the requirements file

    $ mkvirtualenv rest && cd rest
    $ pip install -r requirements.txt

* Start the server. The server is a tornado server (a simple and elegant HTTP server).

    $ python main.py

* Open http://127.0.0.1:8000 in your browser
* The following URLs are accessible
    * http://127.0.0.1:8000/
    * http://127.0.0.1:8000/word (PUT only)
    * http://127.0.0.1:8000/words (GET only)
    * http://127.0.0.1:8000/words/<word> (GET only)
