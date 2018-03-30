from pymongo import MongoClient

from gem.db.proposals import ProposalsRepository
from gem.db.roles import RolesRepository
from gem.db.users import UsersRepository
from gem.db.ballot import BallotsRepository


class GemDatabase:
    """
    GEM's Database
    """

    def __init__(self, host, port, db_name):
        """
        Initializes new instance of the GemDatabase class.
        :param host: Host of MongoDb instance
        :param port: Port of MongoDb instance
        :param db_name: Database name
        """
        self.__db_name = db_name
        self.__client = MongoClient(host, port)
        self.__database = self.__client[db_name]

    def drop(self):
        """
        Drops whole database
        """
        self.__client.drop_database(self.__db_name)

    @property
    def proposals(self):
        """
        Returns proposals repository
        :rtype: ProposalsRepository
        :return: Repository
        """
        return ProposalsRepository(self.__database["proposals"])

    @property
    def users(self):
        """
        Returns users repository
        :rtype: UsersRepository
        :return: Repository
        """
        return UsersRepository(self.__database["users"])

    @property
    def roles(self):
        """
        Returns roles repository
        :rtype: RolesRepository
        :return: Repository
        """
        return RolesRepository(self.__database["roles"])

    @property
    def ballots(self):
        """
        Returns roles repository
        :rtype: RolesRepository
        :return: Repository
        """
        return BallotsRepository(self.__database["ballots"])
