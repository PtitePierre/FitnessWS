from flask import Flask
from flask import jsonify
from flask import request
# import MySQLdb
from flask.ext.mysql import MySQL


app = Flask(__name__)


def connect():
    """connect user to DataBase on host"""
    host = "psotty.mysql.pythonanywhere-services.com"
    user = "psotty"
    pswd = ""
    # or psotty$fitness
    database = "psotty$fitness"
    """
    db = MySQLdb.connect(host, user, pswd, database)
    """
    mysql = MySQL()

    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = user
    app.config['MYSQL_DATABASE_PASSWORD'] = pswd
    app.config['MYSQL_DATABASE_DB'] = database
    app.config['MYSQL_DATABASE_HOST'] = host
    mysql.init_app(app)
    db = mysql.connect()

    return db


@app.route("/")
def hello():
    return "Hello World !"


# TO DO : GET Units
@app.route('/units', methods=['GET'])
def getAllUnits():
    units = []
    db = connect()
    cursor = db.cursor()

    sql = "SELECT * FROM unit"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            unit = {
                'id': row[0],
                'name': row[1],
                'code': row[2]
            }
            units.append(unit)
    except:
        print("Error: unable to fecth data")

    # disconnect from server
    db.close()

    return jsonify({'units': units})


# TO DO : GET SportType
@app.route('/sports', methods=['GET'])
def getAllSports():
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM sport"

    sports = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            sport = {
                'id': row[0],
                'name': row[1],
            }
            sports.append(sport)
    except:
        print("Error: unable to fecth data")

    # disconnect from server
    db.close()

    return jsonify({"sports": sports})


# TO DO : GET Session with specific id
@app.route('/sessions/<user>', methods=['GET'])
def getAllSessionsOfUser(user):
    userid = request.json['id']  # or user ~
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM session WHERE user_id = '%d'" % (userid)
    sessions = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            session = {
                'id': row[0],
                'name': row[1],
            }
            sessions.append(session)
    except:
        print("Error: unable to fecth data")

    # disconnect from server
    db.close()

    return jsonify(sessions)


@app.route('/units', methods=['POST'])
def createUnit():
    unit = {
        'name': request.json['name'].lower(),
        'code': request.json['code'].lower()
    }
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO unit(name, code) \
       VALUES ('%s', '%s')" % (unit['name'], unit['code'])
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

    return getAllUnits()


@app.route('/sports', methods=['POST'])
def createSport():
    sport = {
        'name': request.json['name'].lower()
    }
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO sport(name) \
       VALUES ('%s')" % (sport['name'])
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
    
    links = []

    return getAllSports()


@app.route('/sessions/<user>', methods=['POST'])
def createSession(user):
    """
    sport_id = db.sports.find({'name': request.json['sport_name']}).sport_id
    unit_id = db.units.find({'code': request.json['unit_code']}).unit_id
    user_id = db.users.find({'name': user}).user_id
    """
    session = {
        'id': request.json['id'],
        'sport_id': sport_id,
        'quantity': request.json['quantity'].lower(),
        'unit_id': unit_id,
        'user_id': user_id
    }
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO session(name) \
       VALUES ('%s', '%s')" % (session['name'])
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

    return getAllSessionsOfUser(user)


@app.route('/users', methods=['POST'])
def createUser():
    user = {
            'name': request.json['name'],
            'mail': request.json['mail'],
            }
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO user(name, email) \
       VALUES ('%s', '%s')" % (user['name'], user['email'])
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
    return user


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)
