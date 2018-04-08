import com from '@/lib/communication';

export default {
  connect() {
    com.set(this.$socket);

    const { $store } = this;
    const token = localStorage.getItem('token');

    // user is connected
    this.$store.dispatch('meeting/connection/setConnectionState', {
      connected: true
    });

    // no authentication found
    // seems to be user is not authenticated
    if (!token) {
      $store.dispatch('meeting/connection/setHandshakeState', {
        success: false,
        message: 'You are not logged in.'
      });
      return;
    }

    // send handshake
    this.$socket.emit('handshake', { token }, response => {
      $store.dispatch('meeting/connection/setHandshakeState', response);

      // meta is not sent if handshake failed
      if (response.state) {
        $store.dispatch('meeting/user', response.user);
        $store.dispatch('meeting/meetingState', response.state);
        $store.dispatch('meeting/meetingProposals', response.state.proposals);
      }
    });
  },
  disconnect() {
    this.$store.dispatch('meeting/connection/setConnectionState', {
      connected: false,
      message: 'Connection lost'
    });
  },
  connect_error() {
    this.$store.dispatch('meeting/connection/setConnectionState', {
      connected: false,
      message: 'Unable to connect'
    });
  },
  stage(data) {
    console.log('stage');

    // information about the state of the stage has arrived.
    // { index: stageIndex, state: {} }
    this.$store.dispatch('meeting/meetingStage', data);
  }
};
