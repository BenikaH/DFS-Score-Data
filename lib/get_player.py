from DB import DB

"""
Gets the player id given the name, or name given the id
"""


def get_table_name(pos):
    if (pos is not None) and (pos.lower in ['p', 'pitcher']):
        return 'rguru_pitchers'
    else:
        return 'rguru_hitters'


def id_from_name(name, pos=None):
    db = DB()
    q = "SELECT id FROM {} WHERE name = %s LIMIT 1".format(get_table_name(pos))
    return db.query_one(q, name)


def name_from_id(id_, pos=None):
    db = DB()
    q = "SELECT name FROM {} WHERE id = %s LIMIT 1".format(get_table_name(pos))
    return db.query_one(q, id_)