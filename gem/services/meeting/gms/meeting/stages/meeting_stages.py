""""MeetingStages - meeting stages container."""

from gem.core import Event


class MeetingStages:
    """Meeting stages container."""

    def __init__(self):
        """Initializes new instance of the MeetingStages class."""
        self.__stages = []  # array of stages
        self.__index = 0  # index of active stage

        self.__switched = Event()
        self.__changed = Event()

    @property
    def all(self):
        """
        Returns list of all stages.

        Returns:
            [list] -- List of stages.
        """
        return self.__stages

    @property
    def current(self):
        """
        Returns current stage.

        Returns:
            MeetingStage -- Current stage.
        """
        if not self.__stages:
            return None  # return None if no stages added
        return self.__stages[self.__index]

    @property
    def index(self):
        """
        Returns index of current stage.

        Returns:
            int -- Index of the stage.
        """
        return self.__index

    @property
    def switched(self):
        """
        Calls after switching to another stage.

        Returns:
            Event -- Event.
        """
        return self.__switched

    @property
    def changed(self):
        """
        Calls on any stage changed.

        Returns:
            Event -- Event.
        """
        return self.__changed

    def switch_to(self, index):
        """
        Switch to stage using specified index.

        Arguments:
            index {int} -- Index of stage.

        Raises:
            ValueError -- If index out of bounds.
        """
        # Index not changed, do nothong
        if index == self.index:
            return

        # check index range
        if index < 0:
            raise ValueError("Index can not be negative")

        if index > len(self.__stages) - 1:
            raise ValueError("Stage index out of bounds")

        # switch to stage using specified index
        self.current.on_leave()
        self.__index = index
        self.current.on_enter()
        self.switched.notify(index, self.current)

        return self.current

    def append(self, stage):
        """
        Appends stage to the meeting.

        Arguments:
            stage {MeetingStage} -- Stage of the meeting to append.

        Raises:
            Exception -- If stage was previously appended.
        """
        # do not allow to append one stage twice
        if stage in self.__stages:
            raise Exception("Stage already present")

        # we need to handle all stage "changed" events to
        # sync it with client, so subscribe specified
        # stage to the __on_stage_changed handler
        def __handler():
            index = self.__stages.index(stage)
            self.__on_stage_changed(index, stage)
        stage.changed.subscribe(__handler)

        # append stage
        self.__stages.append(stage)

    def __on_stage_changed(self, index, stage):
        """
        On meeting stage changed

        Arguments:
            index {int} -- Index of the stage.
            stage {MeetingStage} -- Stage.
        """
        self.changed.notify(index, stage)

    def __getitem__(self, key):
        return self.__stages[key]
