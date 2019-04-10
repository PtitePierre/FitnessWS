from flask import Flask
from flask import jsonify
from flask import request
# import MySQLdb
from flask.ext.mysql import MySQL


app = Flask(__name__)

# TODO : remplacer les print de debugg par des ecritures fichier
# --> fichier de logging/debugg pour conserver des traces du fonctionnement
# ajouter des commentaires clairs > doc string

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
    err = 201
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
        err = 404

    get_sport = "SELECT id FROM sport WHERE name LIKE '%s'" % (sport['name'])
    try:
        cursor.execute(get_sport)
        sport_id = cursor.fetchone()[0]

        for unit_id in units:
            # unit_id = unit['unit_id']
            sql = "INSERT INTO sport_unit(sport_id, unit_id) \
               VALUES ('%d', '%d')" % (sport_id, unit_id)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                err = 404
    except Exception as inst:
        print("Error: unable to insert links between sport & unit")
        print(inst.args)
        err = 404

    db.close()
    return jsonify({'ERR': err})


# TO DO : INSERT user
@app.route('/users', methods=['POST'])
def createUser():
    if(request.json['name'] != "" and
       request.json['email'] != "" and
       request.json['password'] != ""):
        user = {
                'name': request.json['name'],
                'email': request.json['email'],
                'h_pwd': request.json['password']
                }
        db = connect()
        cursor = db.cursor()
        sql = "INSERT INTO user(name, email, h_pwd) \
           VALUES ('%s', '%s', '%s')"\
           % (user['name'], user['email'], user['h_pwd'])
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
            user = {'ERR': 'unable to insert '+request.json['name']}

        # disconnect from server
        db.close()
    else:
        user = {'ERR': 'incomplet data'}
    return jsonify(user)


# GET user_id
@app.route('/users/<user_name>', methods=['GET'])
def getUserID(user_name):

    db = connect()
    cursor = db.cursor()
    sql = "SELECT id, name, email, h_pwd FROM user \
    WHERE name = '%s'" % (user_name)

    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        user = {
                "id": res[0],
                "name": res[1],
                "email": res[2],
                "password": res[3]
                }

    except:
        print("Error: unable to fecth data in sport")

    db.close()
    return jsonify(user)


# TO DO : GET Session with specific user's id
@app.route('/sessions/<user_id>', methods=['GET'])
def getAllSessionsOfUser(user_id):
    usr = int(user_id)
    db = connect()
    cursor = db.cursor()
    sql = "SELECT id, sport_unit_id, s_date, quantity, done, weight, wunit \
    FROM session WHERE user_id = '%d'" % (usr)
    sessions = []

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            get_sport_unit = "SELECT sport_id, unit_id FROM sport_unit \
            WHERE id = '%d'" % (row[1])
            try:
                cursor.execute(get_sport_unit)
                res = cursor.fetchall()
                for line in res:
                    sport_id = line[0]
                    unit_id = line[1]
            except:
                print("Error: unable to get sport & unit id from sport_unit")

            session = {
                'id': row[0],
                'quantity': row[3],
                'sunit_id': unit_id,
                'sDate': row[2],
                'stype_id': sport_id,
                'done': row[4],
                'weight': row[5],
                'wunit': row[6],
                'user_id': user_id,
            }
            sessions.append(session)
    except:
        print("Error: unable to fecth data in session")

    db.close()
    return jsonify(sessions)


# TO DO : INSERT session with specific user
@app.route('/sessions', methods=['POST'])
def createSession():
    err = 201
    # from the method's body
    # get the new session
    # get the sending user
    sport_id = request.json['stype_id']
    unit_id = request.json['sunit_id']
    user_id = request.json['user_id']
    s_date = request.json['sdate']
    quantity = request.json['quantity']
    weight = request.json['weight']
    wunit = request.json['wunit']
    done = request.json['done']

    db = connect()
    cursor = db.cursor()

    sql_id_sportunit = "SELECT id FROM sport_unit \
        WHERE sport_id = '%d' AND unit_id = '%d'" % (sport_id, unit_id)

    try:
        cursor.execute(sql_id_sportunit)
        sport_unit_id = cursor.fetchone()[0]
    except:
        print("Error: unable to get sport_unit_id")
        err = 404
    """
    sql = "INSERT INTO session \
        (s_date, quantity, user_id, sport_unit_id, done, weight, wunit) \
        VALUES \
        ('%s', '%d', '%d', '%d', '%d', '%d', '%s')" % (s_date, quantity,
        user_id, sport_unit_id, done, weight, wunit)
    """
    sql = "INSERT INTO session \
        (s_date, quantity, user_id, sport_unit_id, done, weight, wunit) \
        VALUES (\""+s_date+"\","+str(quantity)+","+str(user_id)+","+str(sport_unit_id)+","+str(done)+","+str(float(weight))+",\""+str(wunit)+"\")"
    
    print(sql)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        print("## OK NEW SESSION ADDED")
    except:
        # Rollback in case there is any error
        db.rollback()
        print("Error: unable to insert new session")
        err = 404
    # disconnect from server
    db.close()
    return getAllSessionsOfUser(user_id)


if __name__ == '__main__':
    app.secret_key = 'dfslhfhdah g;hg;dfhgdfhgdf;hgdfahg;hgrggfdgdaf;'
    app.run(debug=True)
