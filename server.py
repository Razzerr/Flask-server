import sys, time
from flask import Flask, jsonify, request
from SQLModule import SQLConnector
from ServerConstants import *

app = Flask(__name__)
conn = None
DBData = []

def startApp(address, login, password, database):
    global conn
    global DBData
    try:
        conn = SQLConnector(address, login, password, database)
        DBData = [address, login, password, database]
    except Exception as e:
        print(str(e))
        sys.exit()
    	
    app.run(debug=True, host='0.0.0.0')

### General functions

def checkListExists(name):
    """
    Checks if a list with provided name exists in the database.
    """
    res = conn.select(SQLCommands["selectList"], (name,))
    return (True if len(res) == 1 else False)
        

def checkItemExists(id):
    """
    Checks if an item with provided list name and id exists in the database.
    """
    res = conn.select(SQLCommands["selectItem"], (id,))
    return (True if len(res) == 1 else False)
    
### /restartDB
@app.route('/restartDB', methods=['GET'])
def restartApp():
    global conn
    global DBData
    try:
        conn = SQLConnector(DBData[0], DBData[1], DBData[2], DBData[3])
        return "", 200
    except Exception as e:
        print(str(e))
        return "", 418

### /lists

@app.route('/lists', methods=['GET'])
def listsGet():
    """
    Tries to fetch a list of checklists.
    """
    try:
        res = conn.select(SQLCommands["selectLists"], ())
        return jsonify([checklist[0] for checklist in res]), 200
    except Exception as e:
        print(str(e))
        return "", 418


@app.route('/lists', methods=['POST'])
def listCreate():
    """
    Checks if a checklist with provided name already exists. If it doesn't, creates a new one.
    """
    rq = str(request.json)
    if len(rq) == 0:
        return jsonify("Empty name provided"), 400

    try:
        if checkListExists(rq):
            return "", 409
        conn.execute(SQLCommands["createList"], (rq,))
        return "", 201
    except Exception as e:
        print(str(e))
        return "", 418

### /lists/{name}

@app.route('/lists/<name>', methods=['DELETE'])
def listDelete(name):
    """
    Checks if a list with provided name exists. If it does, deletes the list.
    """
    if len(name) == 0:
        return jsonify("You have to privde an ID."), 404

    try:
        if not checkListExists(name):
            return "", 404
        conn.execute(SQLCommands["deleteLItems"], (name,))
        conn.execute(SQLCommands["deleteList"], (name,))
        return "", 200
    except Exception as e:
        print(str(e))
        return "", 418

### /lists/{name}/items

@app.route('/lists/<name>/items', methods=['GET'])
def itemGet(name):
    """
    Checks if a checklist with provided name exists, then returns a list of it's items.
    """

    if len(name) == 0:
        return jsonify("You have to privde an ID."), 404
    
    try:
        if not checkListExists(name):
            return "", 404

        res = conn.select(SQLCommands["selectItems"], (name,))
        return jsonify([{"name" : item[0], 
                         "checked" : True if item[1] == 1 else False}
                          for item in res]), 200
    except Exception as e:
        print(str(e))
        return "", 418

@app.route('/lists/<name>/items', methods=['POST'])
def itemAdd(name):
    """
    Checks if a provided checklist exists. If it does, it adds a new item to the checklist and returns
    it's id.
    """
    rq = request.json
    if len(rq) == 0:
        return jsonify("No name provided"), 400

    try:
        if not checkListExists(name):
            return "", 404

        res = conn.select(SQLCommands["selectMaxID"], (name,))
        nextID = 1 if (res[0][0] == None) else (res[0][0] + 1)
        conn.execute(SQLCommands["createItem"], (nextID, name, rq,))
        return jsonify(nextID), 201
    except Exception as e:
        print(str(e))
        return "", 418

### /lists/{name}/items/{id}

@app.route('/lists/<name>/items/<id>', methods=['PATCH'])
def itemChangeState(name, id):
    """
    Checks if provided checklist and an item of given exist. If so, alters the 'checked' property as provided in the request.
    """
    rq = request.json
    if rq not in [True, False]:
        return jsonify("Wrong request content"), 400

    try:
        if not checkListExists(name) or not checkItemExists(id):
            return "", 404

        conn.execute(SQLCommands["chStateItem"], (1 if rq else 0, id,))
        return "", 202
    except Exception as e:
        print(str(e))
        return "", 418

@app.route('/lists/<name>/items/<id>', methods=['DELETE'])
def itemDelete(name, id):
    """
    Checks if provided checklist and an item of given ID exist. If so, deletes the item.
    """
    try:
        if not checkListExists(name) or not checkItemExists(id):
            return "", 404

        conn.execute(SQLCommands["deleteItem"], (id,))
        return "", 200
    except Exception as e:
        print(str(e))
        return "", 418
