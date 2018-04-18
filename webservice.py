from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient

app = Flask(__name__)


units = [
{
    'name':'kilometer',
'code':'km'
},
{
    'name':'minute',
    'code':'min'
}]

client = MongoClient()
db = client.units


@app.route("/")
def hello():
    return "Hello World !"


# TO DO : GET Units
@app.route('/units',methods=['GET'])
def getAllUnits():
    res = db.units.find({})
    units = []
    for unit in res:
        units.append(str(unit))

    res_unit = jsonify({'units':units})

    return res_unit


# TO DO : GET SportType
@app.route('/sports',methods=['GET'])
def getAllSports():
    res = db.sports.find({})
    sports = []
    for sport in res:
        sports.append(str(sport))

    res_sport = jsonify({"sports":sports})
    return res_sport


# TO DO : GET Session with specific id
@app.route('/sessions/<id>',methods=['GET'])
def getAllSessionsOfUser():
    sessions = []
    return sessions


@app.route('/units',methods=['POST'])
def createUnit():
    unit = {
    'id':request.json['id'],
    'name':request.json['name'],
    'code':request.json['code']
    }
    db.units.insert(unit)
    return getAllUnits()


@app.route('/sports',methods=['POST'])
def createSport():
    sport = {
    'id':request.json['id'],
    'name':request.json['name']
    }
    db.sports.insert(sport)
    return getAllSports()


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)