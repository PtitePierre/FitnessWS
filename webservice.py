from flask import Flask
from flask import jsonify
from flask import request
import MySQLdb


def connect():
    """connect user to DataBase on host"""
    db = MySQLdb.connect("host","user","pswd","DataBase")
    return db

def insertUnit(u_name, u_code):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO UNIT(NAME, \
       CODE) \
       VALUES ('%s', '%s')" % \
       (u_name, u_code)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

    # disconnect from server
    db.close()


@app.route("/")
def hello():
    return "Hello World !"


# TO DO : GET Units
@app.route('/units', methods=['GET'])
def getAllUnits():
    db = connect()
    cursor = db.cursor()

    sql = "SELECT * FROM UNIT"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
        units = []
       for row in results:        
            unit = {
                'name': row[0],
                'code': row[1]
            }
            units.append(unit)
    except:
       print "Error: unable to fecth data"

    # disconnect from server
    db.close()
    """
    client = MongoClient()
    db = client.fitness
    res = db.units.find({})
    units = []

    for unit in res:
        units.append(str(unit))
    """
    return jsonify({'units': units})


# TO DO : GET SportType
@app.route('/sports', methods=['GET'])
def getAllSports():
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM SPORT"
    """
    client = MongoClient()
    db = client.fitness
    res = db.sports.find({})
    """
    sports = []

    for sport in res:
        sports.append(str(sport))
    return jsonify({"sports": sports})


# TO DO : GET Session with specific id
@app.route('/sessions/<user>', methods=['GET'])
def getAllSessionsOfUser(user):
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM SESSION WHERE USERID = '%d'" %(userid)
    """
    client = MongoClient()
    db = client.fitness
    user_id = db.users.find({'name': user})
    res = db.sessions.find({'user_id': user_id})
    """
    sessions = []

    for session in res:
        sessions.append(str(session))

    return jsonify(sessions)


@app.route('/units', methods=['POST'])
def createUnit():
    unit = {
        'id': request.json['id'],
        'name': request.json['name'].lower(),
        'code': request.json['code'].lower()
    }
    db.units.insert(unit)
    return getAllUnits()


@app.route('/sports', methods=['POST'])
def createSport():
    sport = {
        'id': request.json['id'],
        'name': request.json['name'].lower()
    }
    db.sports.insert(sport)
    return getAllSports()


@app.route('/sessions/<user>', methods=['POST'])
def createSession(user):
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
    user = {
            'name': request.json['name'],
            'mail': request.json['mail'],
            }
    db.users.insert(user)
    return user


app = Flask(__name__)


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)
