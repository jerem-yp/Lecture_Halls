from fastapi import FastAPI
from configparser import ConfigParser
from pathlib import Path

from db_connection import Database_Querying

app = FastAPI()

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

@app.get('/{day}/{building}')
async def get_building(day: str, building: str):
    """ Get all classes for the day of the week. """
    day = day.title()
    building = building.upper()  # Will only recognize uppercased buildings
    return Database_Querying().get_building(building, day)

@app.get('/{day}/{building}/{room}')
async def get_room(day: str, building: str, room: str):
    """ Get all classes for a location for a day of the week."""
    day = day.title()
    building = building.upper()
    if not room.isnumeric():
        return []
    else:
        return Database_Querying().get_single_room(building=building, room=room, day=day)

@app.get('/all-classrooms')
async def all_classrooms():
    """ Return all classrooms. """
    return Database_Querying().get_all_classrooms()

@app.get('/all-buildings')
async def all_buildings():
    """ Return all buildings. """
    return Database_Querying().get_all_buildings()

