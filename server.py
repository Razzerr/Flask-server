from flask import Flask, jsonify, request
from SQLModule import SQLConnector

app = Flask(__name__)

conn = SQLConnector('localhost', 'root', '!C75dcdc', 'restfullists')

sqlCommands = {
    "selectLists" : "SELECT * FROM `lists`;",
    "selectList"  : "SELECT `name` FROM `lists` WHERE `name` = %s;",
    "selectItems" : "SELECT `name`, `checked` FROM `items` where `list` = %s;",
    "selectItem"  : "SELECT `name` FROM `items` WHERE `ID` = %s;",
    "selectMaxID" : "SELECT MAX(`ID`) FROM `items` WHERE `list` = %s",
    "createList"  : "INSERT INTO `lists` VALUES (%s);",
    "deleteList"  : "DELETE FROM `lists` WHERE (`name` = %s);",
    "deleteLItems": "DELETE FROM `items` WHERE (`list` = %s);",
    "createItem"  : "INSERT INTO `items` (`ID`, `list`, `name`) VALUES (%s, %s, %s);",
    "chStateItem" : "UPDATE `items` SET `checked` = %s WHERE (`ID` = %s);",
    "deleteItem"  : "DELETE FROM `items` WHERE (`ID` = %s);"
}

### General functions

def checkListExists(name):
    """
    Checks if a list with provided name exists in the database.
    """
    res = conn.select(sqlCommands["selectList"], (name,))
    if res[0]:
        if len(res[1]) != 1:
            return (False, ("", 404))
    else:
        return (False, (jsonify(res[1]), 418))
    return (True, ("", ""))

def checkItemExists(id):
    """
    Checks if an item with provided list name and id exists in the database.
    """
    res = conn.select(sqlCommands["selectItem"], (id,))
    if res[0]:
        if len(res[1]) != 1:
            return (False, ("", 404))
    else:
        return (False, (jsonify(res[1]), 418))
    return (True, ("", ""))

### /lists

@app.route('/lists', methods=['GET'])
def listsGet():
    """
    Tries to fetch a list of checklists.
    """
    res = conn.select(sqlCommands["selectLists"], ())
    if res[0]:
        return jsonify([checklist[0] for checklist in res[1]]), 200
    return jsonify(res[1]), 418

@app.route('/lists', methods=['POST'])
def listCreate():
    """
    Checks if a checklist with provided name already exists. If it doesn't, creates a new one.
    """
    if not request.json:
        return jsonify("No request provided"), 400

    rq = str(request.json)
    if len(rq) == 0:
        return jsonify("Empty name provided"), 400

    res = checkListExists(rq)
    if res[0]:
        return "", 409

    res = conn.execute(sqlCommands["createList"], (rq,))
    if res[0]:
        return "", 201
    return jsonify(res[1]), 418

### /lists/{name}

@app.route('/lists/<name>', methods=['DELETE'])
def listDelete(name):
    """
    Checks if a list with provided name exists. If it does, deletes the list.
    """
    if len(name) == 0:
        return jsonify("You have to privde an ID."), 404

    res = checkListExists(name)
    if not res[0]:
        return "", 404

    res = conn.execute(sqlCommands["deleteList"], (name,))
    if res[0]:
        res = conn.execute(sqlCommands["deleteLItems"], (name,))
        if res[0]:
            return "", 200
    return jsonify(res[1]), 418

### /lists/{name}/items

@app.route('/lists/<name>/items', methods=['GET'])
def itemGet(name):
    """
    Checks if a checklist with provided name exists, then returns a list of it's items.
    """
    res = checkListExists(name)
    if not res[0]:
        return res[1]

    res = conn.select(sqlCommands["selectItems"], (name,))
    if res[0]:
        final = []
        for item in res[1]:
            temp = {}
            temp["name"] = item[0]
            temp["checked"] = True if item[1] == 1 else False
            final += [temp]
        return jsonify(final), 200
    return jsonify(res[1]), 418

@app.route('/lists/<name>/items', methods=['POST'])
def itemAdd(name):
    """
    Checks if a provided checklist exists. If it does, it adds a new item to the checklist and returns
    it's id.
    """
    if not request.json:
        return jsonify("No request provided"), 400

    rq = request.json
    if len(rq) == 0:
        return jsonify("No name provided"), 400

    res = checkListExists(name)
    if not res[0]:
        return res[1]

    res = conn.select(sqlCommands["selectMaxID"], (name,))
    if res[0]:
        nextID = 1 if (res[1][0][0] == None) else (res[1][0][0] + 1)
        res = conn.execute(sqlCommands["createItem"], (nextID, name, rq,))
        if res[0]:
            return jsonify(nextID), 201
    return jsonify(res[1]), 418

### /lists/{name}/items/{id}

@app.route('/lists/<name>/items/<id>', methods=['PATCH'])
def itemChangeState(name, id):
    """
    Checks if provided checklist and an item of given exist. If so, alters the 'checked' property as provided in the request.
    """
    rq = request.json
    if rq not in [True, False]:
        return jsonify("Wrong request content"), 400

    res = checkListExists(name)
    if not res[0]:
        return res[1]

    res = checkItemExists(id)
    if not res[0]:
        return res[1]

    res = conn.execute(sqlCommands["chStateItem"], (1 if rq else 0, id,))
    if res[0]:
        return "", 202
    return jsonify(res[1]), 418

@app.route('/lists/<name>/items/<id>', methods=['DELETE'])
def itemDelete(name, id):
    """
    Checks if provided checklist and an item of given ID exist. If so, deletes the item.
    """
    res = checkListExists(name)
    if not res[0]:
        return res[1]

    res = checkItemExists(id)
    if not res[0]:
        return res[1]

    res = conn.execute(sqlCommands["deleteItem"], (id,))
    if res[0]:
        return "", 200
    return jsonify(res[1]), 418

if __name__ == '__main__':
    app.run(debug=True)