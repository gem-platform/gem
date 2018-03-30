from gem.db.core import Model, Repository, Mapper


class Proposal(Model):
    """
    Proposal document
    """

    def __init__(self, index=None, title=None):
        """
        Initializes new instance of the Proposal class.
        """
        super().__init__()
        self.title = title
        self.index = None
        self.content = None


class ProposalsMapper(Mapper):
    """
    Converts proposal db data to Proposal model and vice versa
    """

    def to_model(self, data):
        """
        Converts DB data to Model
        :rtype: Proposal
        :param data: Data to model
        """
        p = Proposal()
        p.id = data.get("_id", None)
        p.title = data.get("title", None)
        p.index = data.get("index", None)
        p.content = data.get("content", None)
        return p

    def to_db(self, model):
        """
        Converts Model to DB data
        :type model: Proposal
        :param model: Proposal to convert
        """
        return {
            "title": model.title,
            "index": model.index,
            "content": model.content
        }


class ProposalsRepository(Repository):
    """
    Proposals repository
    """

    def __init__(self, collection):
        """
        Initialize new instance of the ProposalsRepository class.
        :param collection: Collection to get data from
        """
        super().__init__(collection, ProposalsMapper())

    def find_by_title(self, title):
        """
        Returns list of proposal found by title
        :rtype: list[Proposal]
        :type title: str
        :param title: Title to find bytes
        """
        return self.find_many({"title": title})

    def find_by_index(self, index):
        """
        Returns  proposal found by index
        :rtype: Proposal
        :type index: str
        :param index: Title to find by
        """
        return self.find_one({"index": index})
