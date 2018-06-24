export default {
  mounted() {
    this.$socket.on('disconnect', this.connectionStageChanged('disconnected', 'Connection lost'));
    this.$socket.on('connect_error', this.connectionStageChanged('disconnected', 'Unable to connect'));
    this.$socket.on('reconnect', this.reconnect);
    this.$socket.on('stage', this.stage);
    this.$socket.on('meeting_status', this.meeting_status);
    this.$socket.on('stage_timer', this.stage_timer);
    this.$socket.on('close', this.close);

    this.sendHandshake();
  },
  beforeDestroy() {
    this.$socket.off('disconnect');
    this.$socket.off('connect_error');
    this.$socket.off('reconnect');
    this.$socket.off('stage');
    this.$socket.off('meeting_status');
    this.$socket.off('stage_timer');
    this.$socket.off('close');
  },
  methods: {
    connectionStageChanged(state, message) {
      return () => {
        this.$store.dispatch('meeting/connection/setConnectionState', {
          state, message
        });
      };
    },
    reconnect() {
      this.sendHandshake();
    },
    stage(data) {
      // information about the state of the stage has arrived.
      // { index: stageIndex, state: {} }
      this.$store.dispatch('meeting/meetingStage', data);

      if (this.$route && !this.$route.path.startsWith('/meeting')) {
        this.$store.dispatch('meeting/attentionRequired', true);
        // todo: looks like is broken now
      }
    },
    stage_timer(data) {
      const now = new Date();
      const ahead = new Date(now.getTime() + (1000 * (data.value || 0)));
      this.$bus.emit('setStageTimer', ahead);
    },

    close() {
      this.$store.dispatch('meeting/close', true);
    },
    sendHandshake() {
      const { token } = this.$auth.user;
      const meetingId = this.$route.params.id;

      // no authentication found
      // seems to be user is not authenticated
      if (!token) {
        this.$store.dispatch('meeting/connection/setConnectionState', {
          state: 'disconnected',
          message: 'You are not logged in.'
        });
        return;
      }

      // send handshake
      this.$socket.emit('handshake', { token, meeting: meetingId }, (response) => {
        // meta is not sent if handshake failed
        if (response.state) {
          this.$store.dispatch('meeting/meetingId', meetingId);
          this.$store.dispatch('meeting/user', response.user);
          this.$store.dispatch('meeting/meetingState', response.state);
          this.$store.dispatch('meeting/meetingProposals', response.state.proposals);
        }

        // set connection state
        this.$store.dispatch('meeting/connection/setConnectionState', {
          state: response.success ? 'connected' : 'disconnected',
          message: response.message
        });
      });

      this.$store.dispatch('meeting/attentionRequired', false);
    }
  }
};
