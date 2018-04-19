from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient
from mongoengine import *

app = Flask(__name__)


class Unit(Document):
    name = StringField(required=True, max_length=200)


@app.route("/")
def hello():
    return "Hello World !"


# TO DO : GET Units
@app.route('/units', methods=['GET'])
def getAllUnits():
    client = MongoClient()
    db = client.fitness
    res = db.units.find({})
    units = []

    for unit in res:
        units.append(str(unit))

    return jsonify({'units': units})


# TO DO : GET SportType
@app.route('/sports', methods=['GET'])
def getAllSports():
    client = MongoClient()
    db = client.fitness
    res = db.sports.find({})
    sports = []

    for sport in res:
        sports.append(str(sport))

    return jsonify({"sports": sports})


# TO DO : GET Session with specific id
@app.route('/sessions/<user>', methods=['GET'])
def getAllSessionsOfUser(user):
    client = MongoClient()
    db = client.fitness
    user_id = db.users.find({'name': user})
    res = db.sessions.find({'user_id': user_id})
    sessions = []

    for session in res:
        sessions.append(str(session))

    return jsonify(sessions)


@app.route('/units', methods=['POST'])
def createUnit():
    client = MongoClient()
    db = client.fitness
    unit = {
        'id': request.json['id'],
        'name': request.json['name'].lower(),
        'code': request.json['code'].lower()
    }
    db.units.insert(unit)
    return getAllUnits()


@app.route('/sports', methods=['POST'])
def createSport():
    client = MongoClient()
    db = client.fitness
    sport = {
        'id': request.json['id'],
        'name': request.json['name'].lower()
    }
    db.sports.insert(sport)
    return getAllSports()


@app.route('/sessions/<user>', methods=['POST'])
def createSession(user):
    client = MongoClient()
    db = client.fitness
    sport_id = db.sports.find({'name': request.json['sport_name']}).sport_id
    unit_id = db.units.find({'code': request.json['unit_code']}).unit_id
    user_id = db.users.find({'name': user}).user_id

    session = {
        'id': request.json['id'],
        'sport_id': sport_id,
        'quantity': request.json['quantity'].lower(),
        'unit_id': unit_id,
        'user_id': user_id
    }
    db.sessions.insert(session)

    return getAllSessionsOfUser(user)


@app.route('/users', methods=['POST'])
def createUser():
    client = MongoClient()
    db = client.fitness
    user = {
            'name': request.json['name'],
            'mail': request.json['mail'],
            }
    db.users.insert(user)
    return user


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)
