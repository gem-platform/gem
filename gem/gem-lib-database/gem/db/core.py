from bson import ObjectId
from abc import ABCMeta, abstractmethod


class Mapper(metaclass=ABCMeta):
    """
    Maps DB data to Model and vice versa
    """

    @abstractmethod
    def to_model(self, data):
        """
        Converts DB data to Model
        :rtype: Model
        :param data: Data to model
        """
        pass

    @abstractmethod
    def to_db(self, model):
        """
        Converts Model to DB data
        :type model: Model
        :param model: Model to convert
        """
        pass


class Model(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        """
        Initializes new instance of Model class
        """
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


class Repository:
    """"""

    def __init__(self, collection, mapper):
        """
        Initializes new instance of the Repository class
        :type mapper: Mapper
        :param collection: Collection to get data from
        :param mapper: Mapper to convert db data to Model and vice versa
        """
        self.__mapper = mapper
        self.__collection = collection

    def count(self, query):
        """
        Returns the number of entities that satisfy the specified query
        :rtype: int
        :type query: dict
        :param query: Query
        :return: Number of records
        """
        return self.__collection.count(query)

    def all(self):
        """
        Returns all entities
        :rtype: list
        :return: List of entities
        """
        return self.__find({})

    def get(self, oid):
        """
        Returns model with specified Id
        :rtype: Model
        :param oid: Model Id
        :return: Model if found, otherwise None
        """
        return self.__get(oid)

    def find_one(self, query):
        """
        Returns one model that satisfy specified query, None if nothing found
        :rtype: Model
        :param query: Query
        :return: Model or None
        """
        return self.__find_one(query)

    def find_many(self, query):
        """
        Returns a list of records that satisfy the specified query
        :rtype: list[Model]
        :param query: Query
        :return: List of entities
        """
        return self.__find(query)

    def save(self, model):
        """
        Inserts new model into DB
        :param model: Model to insert
        """
        if model.id is None:
            db_data = self.__mapper.to_db(model)
            res = self.__collection.insert_one(db_data)
            model.id = res.inserted_id
        else:
            self.__collection.replace_one(
                {"_id": model.id}, self.__mapper.to_db(model))

    def delete(self, oid):
        return self.__collection.find_one_and_delete({
            "_id": ObjectId(oid)
        })

    # internal functions

    def __find(self, query):
        result = []
        dbo = list(self.__collection.find(query))
        for dboobj in dbo:
            result.append(self.__mapper.to_model(dboobj))
        return result

    def __find_one(self, criteria):
        dbo = self.__collection.find_one(criteria)
        return self.__mapper.to_model(dbo)

    def __get(self, oid):
        dbo = self.__collection.find_one(ObjectId(oid))
        return self.__mapper.to_model(dbo)
