"""
File to run when starting the server.
"""

from website import create_app


app = create_app() # creates flask server application object

if __name__ == '__main__':
    app.run(debug=True) # runs flask server application object with live changes