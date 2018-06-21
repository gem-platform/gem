<template>
  <no-ssr>
    <component :is="screen"/>
  </no-ssr>
</template>

<script>
import MeetingScreen from '@/components/meeting/screens/MeetingScreen.vue';
import ConnectingScreen from '@/components/meeting/screens/ConnectingScreen.vue';

export default {
  name: 'GemPlatform',
  layout: 'portal',
  components: {
    MeetingScreen,
    ConnectingScreen
  },
  computed: {
    screen() {
      const hs = this.$store.getters['meeting/connection/state'].state === 'connected';
      return hs ? 'MeetingScreen' : 'ConnectingScreen';
    }
  },
  created() {
    this.$bus.on('notification', this.snackbar);
  },
  beforeDestroy() {
    this.$bus.off('notification', this.snackbar);
  },
  mounted() {
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
  },
  methods: {
    snackbar(data) {
      this.$snackbar.open(data);
    }
  }
};
</script>
