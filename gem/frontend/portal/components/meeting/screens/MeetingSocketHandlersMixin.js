export default {
  mounted() {
    this.$socket.on('disconnect', this.disconnect);
    this.$socket.on('connect_error', this.disconnect);
    this.$socket.on('reconnect', this.reconnect);
    this.$socket.on('stage', this.stage);
    this.$socket.on('stage_timer', this.stage_timer);
    this.$socket.on('close', this.close);

    this.sendHandshake();
  },
  beforeDestroy() {
    this.$socket.off('disconnect', this.disconnect);
    this.$socket.off('connect_error', this.disconnect);
    this.$socket.off('reconnect', this.reconnect);
    this.$socket.off('stage', this.stage);
    this.$socket.off('stage_timer', this.stage_timer);
    this.$socket.off('close', this.close);
  },
  methods: {
    disconnect(reason) {
      this.$store.dispatch('meeting/connection/setConnectionState', {
        state: 'disconnected', message: `Connection failed. ${reason}`
      });
    },
    reconnect() {
      this.sendHandshake();
    },
    stage(data) {
      // information about the state of the stage has arrived.
      // { index: stageIndex, state: {} }
      this.$store.dispatch('meeting/meetingStage', data);
    },
    stage_timer(data) {
      if (data.mode === '=') {
        const now = new Date();
        const ahead = new Date(now.getTime() + (1000 * (data.value || 0)));
        this.$bus.emit('setStageTimer', ahead);
      } else if (data.mode === '+') {
        this.$bus.emit('addStageTimer', data.value);
      }
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
          this.$store.dispatch('meeting/close', false);
        }

        // set connection state
        this.$store.dispatch('meeting/connection/setConnectionState', {
          state: response.success ? 'connected' : 'disconnected',
          message: response.message,
          actions: response.actions
        });
      });
    }
  }
};
