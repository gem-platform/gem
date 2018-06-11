import com from '@/lib/communication';

export default store => ({
  connect() {
    com.set(this.$socket);
  },
  disconnect() {
    this.$store.dispatch('meeting/connection/setConnectionState', {
      state: 'disconnected',
      message: 'Connection lost'
    });
  },
  connect_error() {
    this.$store.dispatch('meeting/connection/setConnectionState', {
      state: 'disconnected',
      message: 'Unable to connect'
    });
  },
  stage(data) {
    // information about the state of the stage has arrived.
    // { index: stageIndex, state: {} }
    store.dispatch('meeting/meetingStage', data);

    if (this.$route && !this.$route.path.startsWith('/meeting')) {
      store.dispatch('meeting/attentionRequired', true);
    }

    // set stage timer
    const now = new Date();
    const ahead = new Date(now.getTime() + (1000 * 60 * 2));
    this.$bus.emit('setStageTimer', ahead);
  },
  meetings_status(data) {
    store.dispatch('meeting/status/set', data);
  }
});
