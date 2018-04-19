import com from '@/lib/communication';

export default store => ({
  connect() {
    com.set(this.$socket);
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
    // information about the state of the stage has arrived.
    // { index: stageIndex, state: {} }
    store.dispatch('meeting/meetingStage', data);

    if (this.$route && this.$route.path !== '/meeting') {
      store.dispatch('meeting/attentionRequired', true);
    }
  }
});
