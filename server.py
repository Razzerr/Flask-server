from flask import Flask, jsonify, abort, make_response, request
from SQLModule import SQLConnector
# from flask_mysqldb import MySQL
app = Flask(__name__)

conn = SQLConnector('localhost', 'root', '!C75dcdc', 'restfullists')

sqlCommands = {
    "selectLists" : "SELECT * FROM `lists`",
    "selectList"  : "SELECT `name` FROM `lists` WHERE `name` = %s",
    "selectItems" : "Select i.`name`, i.`checked` " + 
                    "from `lists` as l right join `items` as i on i.list = l.name " + 
                    "where i.list = %s",
    "selectItem"  : "SELECT `name` FROM `items` WHERE `ID` = %s AND `list` = %s",
    "createList"  : "INSERT INTO `lists` VALUES (%s)",
    "deleteList"  : "DELETE FROM `lists` WHERE (`name` = %s)",
    "createItem"  : "INSERT INTO `items` (`list`, `name`) VALUES (%s, %s)",
    "deleteItem"  : ""
}

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '!C75dcdc'
# app.config['MYSQL_DB'] = 'restfullists'

# mysql = MySQL(app)

### SQL functions

# def SQLFetchLists():
#     """
#     Returns list of names of fetched checklists.
#     """
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM `lists`")
#     lists = cur.fetchall()
#     cur.close()
#     return [listInstance[0] for listInstance in lists]

# def SQLAddList(name):
#     """
#     Adds a new checklist to the database.
#     """
#     if SQLCheckListExists(name):
#         return (False, "Checklist of given name already exists.")
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO `lists` VALUES (%s)", (name,))
#         mysql.connection.commit()
#         return (True, "New checklist inserted.")
#     except Exception as e:
#         mysql.connection.rollback()
#         return (False, str(e))
#     finally:
#         cur.close()

# def SQLDeleteList(name):
#     """
#     Deletes a checklist from the database.
#     """
#     if not SQLCheckListExists(name):
#         return (False, "Checklist of given ID does not exist.")
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("DELETE FROM `lists` WHERE (`name` = %s);", (name,))
#         mysql.connection.commit()
#         return (True, "OK.")
#     except Exception as e:
#         mysql.connection.rollback()
#         return (False, str(e))
#     finally:
#         cur.close()

# def SQLGetItems(name):
#     """
#     Checks if a checklist with provided name exists, then returns a list of it's items.
#     """
#     if not SQLCheckListExists(name):
#         print("DOESNT")
#         return(False, "List with a given ID doesn't exist.")
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("Select i.`name`, i.`checked` " + 
#                     "from `lists` as l right join `items` as i on i.list = l.name " + 
#                     "where i.list = %s", (name,))
#         return (True, "JSON array of checklist's items.", cur.fetchall())
#     except Exception as e:
#         return (False, str(e))
#     finally:
#         cur.close()


def checkListExists(name):
    """
    Checks if a list with provided name exists in the database.
    """
    res = conn.select(sqlCommands["selectList"], (name,))
    if res[0]:
        if len(res[1]) != 1:
            return (False, ("", "404 List does not exist!"))
    else:
        return (False, ("", "400 " + res[1]))
    return (True, ("", ""))

def checkItemExists(name, id):
    """
    Checks if an item with provided list name and id exists in the database.
    """
    res = conn.select(sqlCommands["selectItem"], (id, name,))
    if res[0]:
        if len(res[1]) != 1:
            return (False, ("", "404 Item does not exist!"))
    else:
        return (False, ("", "400 " + res[1]))
    return (True, ("", ""))

### /lists

@app.route('/lists', methods=['GET'])
def listsGet():
    """
    Tries to fetch a list of checklists.
    """
    res = conn.select(sqlCommands["selectLists"], ())
    if res[0]:
        return jsonify([checklist[0] for checklist in res[1]]), ("200 JSON array of checklists' names.")
    return "", "400 " + res[1] 

@app.route('/lists', methods=['POST'])
def listCreate():
    """
    Checks is a checklist with provided name already exists. If it doesn't, creates a new one.
    """
    if not request.json:
        return jsonify("No request provided"), 400

    rq = request.json
    if len(rq) == 0:
        return jsonify("No name provided"), 400

    res = checkListExists(rq)
    if res[0]:
        return "", "409 List already exists"

    res = conn.execute(sqlCommands["createList"], (rq,))
    if res[0]:
        return "", "201 " + res[1] #TO-DO Custom message
    return "", "409 " + res[1]

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
        return res[1]

    res = conn.execute(sqlCommands["deleteList"], (name,))
    if res[0]:
        return "", "200 " + res[1] #TO-DO Custom message
    return "", "404 " + res[1]

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
        print(res[1])
        for item in res[1]:
            temp = {}
            temp["name"] = item[0]
            temp["checked"] = True if item[1] == 1 else False
            final += [temp]
        return jsonify(final), "200 " #TO-DO Custom message
    return "", "409 " + res[1]

@app.route('/lists/<name>/items', methods=['POST'])
def itemAdd(name):
    if not request.json:
        return jsonify("No request provided"), 400

    rq = request.json
    if len(rq) == 0:
        return jsonify("No name provided"), 400

    res = checkListExists(name)
    if not res[0]:
        return res[1]

    res = checkItemExists(name, rq)
    if res[0]:
        return "", "409 Item already exists"

    res = conn.execute(sqlCommands["createItem"], (name, rq,))
    if res[0]:
        return "", "201 " + res[1] #TO-DO Custom message
    return "", "409 " + res[1]

    

#Deleting an item
@app.route('/lists/<lname>/items/<id>', methods=['DELETE'])
def itemDelete(iname, id):
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)