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

        # gets list of online users
        users_online = stage.meeting.sessions.online
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

    def summary_serialize(self, stage):
        """Serialize."""
        if not stage.ballot:
            return {}

        result = {}
        for vote in stage.ballot.votes:
            rid = str(vote.role.id)
            if rid not in result:
                result[rid] = {"yes": 0, "no": 0, "abstained": 0, "users": []}
            result[rid][vote.value] += 1

            if vote.user:
                result[rid]["users"].append({"id": str(vote.user.id), "value": vote.value})
        return {"secret": stage.ballot.secret, "votes": result, "result": stage.ballot.result}

    @staticmethod
    def __users_can_vote(users):
        return list(filter(lambda user: "meeting.vote" in user.permissions, users))
