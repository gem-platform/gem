"""GEM Meeting Server Entry point"""

import logging
import logging.config

from gms.app import MeetingServerApplication
from gms.net import SocketIoEndpoint

logging.config.fileConfig('logging.conf')

logging.getLogger("root").info("GEM Meeting Server is starting")

# configure application endpoints
ENDPOINT = SocketIoEndpoint("0.0.0.0", 8090)

# run app
APP = MeetingServerApplication()
APP.endpoints.add(ENDPOINT)
APP.run()
