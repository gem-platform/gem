import com from '@/communication';

export default {
  connect() {
    com.set(this.$socket);

    const { $store } = this;
    const token = localStorage.getItem('token');

    // user is connected
    this.$store.dispatch('setConnectionState', { connected: true });

    // no authentication found
    // seems to be user is not authenticated
    if (!token) {
      $store.dispatch('setHandshakeState', {
        success: false,
        message: 'You are not logged in.',
      });
      return;
    }

    // send handshake
    this.$socket.emit('handshake', { token }, (response) => {
      $store.dispatch('setHandshakeState', response);

      // meta is not sent if handshake failed
      if (response.state) {
        $store.dispatch('user', response.user);
        $store.dispatch('meetingState', response.state);
        $store.dispatch('meetingProposals', response.state.proposals);
      }
    });
  },
  disconnect() {
    this.$store.dispatch('setConnectionState', {
      connected: false, message: 'Connection lost',
    });
  },
  connect_error() {
    this.$store.dispatch('setConnectionState', {
      connected: false, message: 'Unable to connect',
    });
  },
  stage(data) {
    // information about the state of the stage has arrived.
    // { index: stageIndex, state: {} }
    this.$store.dispatch('meetingStage', data);
  },
};
