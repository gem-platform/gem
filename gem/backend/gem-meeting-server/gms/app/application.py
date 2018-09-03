from gem.core import Application
from gms.app.active_meetings import ActiveMeetings


class MeetingServerApplication(Application):
    """GEM Meeting Server application."""

    def __init__(self):
        """Initialize new instance of the MeetingServerApplication class."""
        super().__init__()
        self.__active_meetings = ActiveMeetings()
        self.__active_meetings.emit.subscribe(self.__on_emit)
        self.__active_meetings.join.subscribe(self.__on_join)
        self.__active_meetings.leave.subscribe(self.__on_leave)
        self.__active_meetings.status_changed.subscribe(
            self.__on_status_changed)

        self.endpoints.event.subscribe(self.__on_endpoint_event)

    def __on_endpoint_event(self, event, *data):
        """
        On endpoint event.

        Arguments:
            event {str} -- Name of the event.

        Returns:
            obj -- Result of the event.
        """
        return self.__active_meetings.command(event, *data)

    def __on_emit(self, event, data, to):
        for endpoint in self.endpoints.all:
            endpoint.emit(event, data, to=to)

    def __on_join(self, sid, room):
        for endpoint in self.endpoints.all:
            endpoint.join(sid, room)

    def __on_leave(self, sid, room):
        for endpoint in self.endpoints.all:
            endpoint.leave(sid, room)

    def __on_status_changed(self):
        for endpoint in self.endpoints.all:
            endpoint.emit("meetings_status", self.__active_meetings.status())
