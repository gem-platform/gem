"""Meeting server application class."""
from os import getenv

from gem.core import Application
from gem.postman import Postman
from gms.app.active_meetings import ActiveMeetings
from gms.app.active_meeting import ActiveMeeting


class MeetingServerApplication(Application):
    """GEM Meeting Server application."""

    def __init__(self):
        """Initialize new instance of the MeetingServerApplication class."""
        super().__init__()

        self.__postman = Postman(sender="info@gem.iskcon.com")

        self.__active_meetings = ActiveMeetings()
        self.__active_meetings.open.subscribe(self.__on_open_meeting)
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

    def __on_open_meeting(self, meeting: ActiveMeeting):
        # connect to SMTP server
        self.__postman.connect(
            getenv('SMTP_HOST', 'localhost'),
            int(getenv('SMTP_PORT', '25'))
        )

        # login if login/password is provided
        if getenv('SMTP_LOGIN'):
            self.__postman.login(
                getenv('SMTP_LOGIN'),
                getenv('SMTP_PASSWORD'),
            )

        # send email to all the users invited to the meeting
        for user in filter(lambda x: x.email, meeting.allowed_users):
            self.__postman.send(user.email, "Meeting is started")

        # all done
        self.__postman.close()

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
