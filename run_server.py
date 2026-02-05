"""
Application entry point for running the Flask development server.

Usage:
  export FLASK_APP=run_server
  flask run

Or with dotenv (e.g. .env with FLASK_APP=run_server):
  flask run
"""
from app import create_app

app = create_app()
