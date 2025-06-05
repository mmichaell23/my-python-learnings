from flask import Flask

app = Flask(__name__)

app.secret_key = 'michaellorenztan'
from app import routes
