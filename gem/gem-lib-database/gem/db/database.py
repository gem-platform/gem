from mongoengine import connect


class GemDatabase:
    """
    GEM's Database
    """

    def __init__(self, db_name):
        connect(db_name)
