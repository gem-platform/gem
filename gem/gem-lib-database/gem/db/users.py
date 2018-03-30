from gem.db.core import Model, Repository, Mapper


class User(Model):
    """
    User
    """

    def __init__(self, name=None):
        """
        Initializes new instance of the User class.
        :type name: str
        :param name: User's name
        """
        super().__init__()
        self.name = name


class UsersMapper(Mapper):
    """
    Converts user db data to User model and vice versa
    """

    def to_model(self, data):
        """
        Converts DB data to Model
        :rtype: User
        :param data: Data to model
        """
        u = User()
        u.id = data.get("_id", None)
        u.name = data.get("name", None)
        return u

    def to_db(self, model):
        """
        Converts Model to DB data
        :type model: User
        :param model: User to convert
        """
        return {
            "name": model.name,
        }


class UsersRepository(Repository):
    """
    Users repository
    """

    def __init__(self, collection):
        """
        Initialize new instance of the UsersRepository class.
        :param collection: Collection to get data from
        """
        super().__init__(collection, UsersMapper())

    def find_by_name(self, name):
        """
        Returns list of users found by name
        :rtype: list[User]
        :type name: str
        :param name: Name to find by
        """
        return self.find_many({"name": name})
