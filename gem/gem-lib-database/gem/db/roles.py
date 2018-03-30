
from gem.db.core import Model, Repository, Mapper


class Role(Model):
    """
    Role
    """

    def __init__(self, name=None):
        """
        Initializes new instance of the Role class.
        :type name: str
        :param name: Name of the role
        """
        super().__init__()
        self.name = name
        self.permissions = []


class RolesMapper(Mapper):
    """
    Converts role db data to Role model and vice versa
    """

    def to_model(self, data):
        """
        Converts DB data to Model
        :rtype: Role
        :param data: Data to model
        """
        r = Role()
        r.id = data.get("_id", None)
        r.name = data.get("name", None)
        r.permissions = data.get("permissions", None)
        return r

    def to_db(self, model):
        """
        Converts Model to DB data
        :type model: Role
        :param model: Role to convert
        """
        return {
            "name": model.name,
            "permissions": model.permissions
        }


class RolesRepository(Repository):
    """
    Roles repository
    """

    def __init__(self, collection):
        """
        Initialize new instance of the RolesRepository class.
        :param collection: Collection to get data from
        """
        super().__init__(collection, RolesMapper())

    def find_by_name(self, name):
        """
        Returns list of role found by name
        :rtype: Role
        :type name: str
        :param name: Name to find by
        """
        return self.find_one({"name": name})
