from Igbot.database.collections import user_ig_accounts


def db_add_ig_acc(user_id, username, password):
    user_id = str(user_id)
    obj_doc = {user_id: {"$exists": True}}
    obj = user_ig_accounts.find_one(obj_doc)
    if obj:
        data = obj[user_id]
        data[username] = password
        update_query = {"$set": {user_id: data}}
        user_ig_accounts.update_one(obj_doc, update_query)
    else:
        data = {user_id: {username: password}}
        user_ig_accounts.insert_one(data)


def db_rm_ig_acc(user_id, username):
    user_id = str(user_id)
    obj_doc = {user_id: {"$exists": True}}
    obj = user_ig_accounts.find_one(obj_doc)
    if obj:
        data: dict = obj[user_id]
        data.pop(username)
        update_query = {"$set": {user_id: data}}
        user_ig_accounts.update_one(obj_doc, update_query)


def db_get_ig_acc(user_id):
    user_id = str(user_id)
    obj_doc = {user_id: {"$exists": True}}
    obj = user_ig_accounts.find_one(obj_doc)
    if obj:
        return obj[user_id]
    else:
        return {}
