class BallotSerializeMixin:
    def progress(self, stage):
        """
        Return progress of the ballot stage.

        Returns:
            float -- Progress in percents.
        """
        # Stage have no ballot
        if not stage.ballot:
            return 0

        # it's impossible to calculate percentage without context
        # (we need: users online) so raise an exception
        if not stage.meeting.context:
            raise Exception("No context provided")

        # gets list of online users using meeting context
        context = stage.meeting.context
        users_online = context.sessions.online
        users_can_vote = self.__users_can_vote(users_online)

        # no one user can vote here
        if len(users_can_vote) <= 0:
            return 0

        # calculate the percentage of completion
        votes_count = len(stage.ballot.votes)
        users_count = len(users_can_vote)
        percent = votes_count / users_count * 100

        # return calculated percent
        return percent

    def votes_serialize(self, stage):
        if stage.ballot.secret:
            return None
        return [{"user_id": str(v.user.id) if v.user else None, "value": v.value} for v in stage.ballot.votes]

    def summary_serialize(self, stage):
        if not stage.ballot:
            return {}

        return self.calculate_votes(stage.ballot.votes)

    @staticmethod
    def __users_can_vote(users):
        return list(filter(lambda user: "meeting.vote" in user.permissions, users))

    @staticmethod
    def calculate_votes(votes):
        result = {}
        for vote in votes:
            rid = str(vote.role.id)
            if rid not in result:
                result[rid] = {"yes": 0, "no": 0, "abstained": 0}
            result[rid][vote.value] += 1
        return result
