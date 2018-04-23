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
    database = "psotty$fitness"

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


# GET Units
@app.route('/units', methods=['GET'])
def getAllUnits():
    units = []
    db = connect()
    cursor = db.cursor()

    sql = "SELECT id, name, code FROM unit"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            unit = {
                'id': row[0],
                'name': row[1],
                'code': row[2],
            }
            units.append(unit)
    except Exception as inst:
        print(inst.args)
        print("Error: unable to fecth data in unit")

    # disconnect from server
    db.close()

    return jsonify({'units': units})


# INSERT unit
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
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to insert unit")

    db.close()
    return getAllUnits()


# GET SportType
@app.route('/sports', methods=['GET'])
def getAllSports():
    db = connect()
    cursor = db.cursor()
    sql = "SELECT id, name FROM sport"

    sports = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:

            getUnits = "SELECT id, unit_id FROM sport_unit \
            WHERE sport_id = '%d'" % (row[0])
            units = []
            try:
                cursor.execute(getUnits)
                res = cursor.fetchall()
                for line in res:
                    units.append(line[1])
            except:
                print("Error: unable to get units id from sport_unit")

            sport = {
                'id': row[0],
                'name': row[1],
                'units': units
            }
            sports.append(sport)
    except:
        print("Error: unable to fecth data in sport")

    db.close()
    return jsonify({"sports": sports})


# INSERT sport in sport db and linked units in sport_unit db
@app.route('/sports', methods=['POST'])
def createSport():
    sport = {
        'name': request.json['name'].lower(),
    }
    units = request.json['units']

    db = connect()
    cursor = db.cursor()
    insert = "INSERT INTO sport(name) \
       VALUES ('%s')" % (sport['name'])
    try:
        cursor.execute(insert)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to insert sport")

    get_sport = "SELECT id FROM sport WHERE name LIKE '%s'" % (sport['name'])
    try:
        cursor.execute(get_sport)
        sport_id = cursor.fetchone()[0]

        for unit in units:
            unit_id = unit['unit_id']
            sql = "INSERT INTO sport_unit(sport_id, unit_id) \
               VALUES ('%d', '%d')" % (sport_id, unit_id)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    except Exception as inst:
        print("Error: unable to insert links between sport & unit")
        print(inst.args)

    db.close()

    return getAllSports()


# TO DO : INSERT user
@app.route('/users', methods=['POST'])
def createUser():
    if(request.json['name'] != "" and
       request.json['email'] != "" and
       request.json['birthday'] != "" and
       request.json['pwd'] != ""):
        user = {
                'name': request.json['name'],
                'email': request.json['email'],
                'birthday': request.json['birthday'],  # check format
                'h_pwd': request.json['pwd']
                }
        db = connect()
        cursor = db.cursor()
        sql = "INSERT INTO user(name, email, birthday, h_pwd) \
           VALUES ('%s', '%s', '%s', '%s')"\
           % (user['name'], user['email'], user['birthday'], user['h_pwd'])
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
            # GET new user id
            get_id = "SELECT id FROM user \
            WHERE name LIKE '%s'" % (user['name'])
            try:
                cursor.execute(get_id)
                user_id = cursor.fetchone()[0]
                user.update({'id': user_id})
            except:
                print("Error: unable to get user id from user")
                user.update({'id': 'ERR: unable to get user id'})

        except Exception as inst:
            # Rollback in case there is any error
            db.rollback()
            print(inst.args)
            user = {'ERR': 'unable to inser '+request.json['name']}

        # disconnect from server
        db.close()
    else:
        user = {'ERR': 'incomplet data'}
    return user


# TO DO : GET Session with specific user's id
@app.route('/sessions', methods=['POST'])
def getAllSessionsOfUser(user):
    user_id = request.json['user_id']  # or user ~
    user_pwd = request.json['user_pwd']
    db = connect()
    cursor = db.cursor()
    sql = "SELECT id, s_date, quantity, sport_unit_id FROM session \
    WHERE user_id = '%d'" % (user_id)
    sessions = []

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            qtt = -1
            sport = -1
            get_sport_unit = "SELECT sport_id, unit_id FROM sport_unit \
            WHERE id = '%d'" % (row[3])
            try:
                cursor.execute(get_sport_unit)
                res = cursor.fetchall()
                for line in res:
                    sport = row[0]
                    qtt = row[1]
            except:
                print("Error: unable to get sport & unit id from sport_unit")

            session = {
                'id': row[0],
                'sDate': row[1],
                'quantity': qtt,
                'sport': sport
            }
            sessions.append(session)
    except:
        print("Error: unable to fecth data in session")

    db.close()
    return jsonify(sessions)


# TO DO : INSERT session with specific user
@app.route('/sessions', methods=['POST'])
def createSession(user):
    """
    sport_id = db.sports.find({'name': request.json['sport_name']}).sport_id
    unit_id = db.units.find({'code': request.json['unit_code']}).unit_id
    user_id = db.users.find({'name': user}).user_id
    """
    # from the method's body
    # get the new session
    # get the sending user

    session = {
        'id': request.json['id'],
        'sport_id': sport_id,
        'quantity': request.json['quantity'].lower(),
        'unit_id': unit_id,
        'user_id': user_id
    }
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO session(s_date,) \
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


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)
