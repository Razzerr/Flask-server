SQLCommands = {
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