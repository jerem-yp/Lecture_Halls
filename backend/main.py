from fastapi import FastAPI
from pydantic import BaseModel
from configparser import ConfigParser
from pathlib import Path

from db_connection import Database_Querying
from retrieve_soc import RetrieveSOC

CONFIG_PATH = "init_files/request.ini"

app = FastAPI()

# For local development, create the database if DNE
config = ConfigParser()
config.read(CONFIG_PATH)
filename = config.get('GLOBAL', 'table_file')
if not Path.exists(Path(filename)):
    create_soc = RetrieveSOC()
    create_soc.call_API()

db = Database_Querying(filename)

""" The FastAPI should only access the database. There are no POST methods to write to this database."""

# @app.get('/{day_of_week}')
# async def get_day_of_week(day_of_week: str):
#     return db.get_all_for_day(day_of_week)
#
# @app.get('/{day_of_week}/{location}')
# async def get_class(day_of_week: str, location: str):
#     return db.get_all_for_class(day_of_week, location)

# command (from backend): uvicorn main:app --reload
# path to SwaggerUI: http://127.0.0.1:8000/docs

@app.get('/')
def hello():
    return 'hello world'

@app.get('/home/{day}')
def get_day_of_week(day: str):
    """ Get all classes for the day of the week. """
    return [x for x in db.get_all_for_day(day=day)]

@app.get('/home/{day}/{class_name}')
def get_day_class(day: str, class_name: str):
    """ Get all classes for a location for a day of the week."""
    day = day.title()
    return [x for x in db.get_all_for_class(day, class_name)]



