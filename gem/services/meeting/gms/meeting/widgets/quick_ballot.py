class QuickBallot():
    """Quick Ballot."""

    def __init__(self):
        """Initializes new instance of a QuickBallot class."""
        self.__result = {}

    def start_new(self):
        """Start a new Quick Ballot."""
        self.__result = {}

    @property
    def results(self):
        """Return results of current ballot."""
        return self.__result

    def vote(self, value):
        """Commit a vote for specified option."""
        if value in self.__result:
            self.__result[value] += 1  # increment count
        else:
            self.__result[value] = 1  # this is a first vote
        return self.results
