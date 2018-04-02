"""GEM Meeting Server Entry point"""
import sys
sys.path.append("../gem-server-common")

from gms.app import MeetingServerApplication
from gms.net import SocketIoEndpoint

print("GEM Meeting Server is starting")

# configure application endpoints
ep = SocketIoEndpoint("0.0.0.0", 8090)

# run app
app = MeetingServerApplication()
app.endpoints.add(ep)
app.run()
