class StagesGroup:
    """Shares state of the stages."""

    def __init__(self, meeting=None, proposal=None):
        """
        Initialize new instance of the StagesGroup class.

        Arguments:
            meeting {Meeting} -- Meeting.

        Keyword Arguments:
            proposal {Proposal} -- Proposal. (default: {None})
        """
        self.__meeting = meeting
        self.__proposal = proposal

    @property
    def meeting(self):
        """
        Return meeting.

        Returns:
            Meeting -- Meeting.
        """
        return self.__meeting

    @property
    def proposal(self):
        """
        Return proposal.

        Returns:
            Proposal -- Proposal.
        """
        return self.__proposal
