"""
This is a simple Flask application that returns a greeting message
when the root endpoint is accessed.
"""

from flask import Flask
from route import routes

app = Flask(__name__)

# Register the routes blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run()