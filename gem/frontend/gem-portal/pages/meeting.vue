<template>
  <div>
    <no-ssr>
      <component :is="screen"/>
    </no-ssr>
  </div>
</template>

<script>
import MeetingScreen from '@/components/screens/MeetingScreen.vue';
import ConnectingScreen from '@/components/screens/ConnectingScreen.vue';

export default {
  name: 'GemPlatform',
  components: {
    MeetingScreen,
    ConnectingScreen
  },
  computed: {
    screen() {
      const hs = this.$store.getters['meeting/connection/state'] === true;
      return hs ? 'MeetingScreen' : 'ConnectingScreen';
    }
  },
  created() {
    this.$bus.on('notification', this.snackbar);
  },
  mounted() {
    const token = this.$auth.user.token;

    // no authentication found
    // seems to be user is not authenticated
    if (!token) {
      this.$store.dispatch('meeting/connection/setHandshakeState', {
        success: false,
        message: 'You are not logged in.'
      });
      return;
    }

    // send handshake
    this.$socket.emit('handshake', { token }, (response) => {
      // meta is not sent if handshake failed
      if (response.state) {
        this.$store.dispatch('meeting/user', response.user);
        this.$store.dispatch('meeting/meetingState', response.state);
        this.$store.dispatch(
          'meeting/meetingProposals',
          response.state.proposals
        );
      }

      this.$store.dispatch('meeting/connection/setHandshakeState', response);
    });
  },
  methods: {
    snackbar(data) {
      this.$snackbar.open(data);
    }
  }
};
</script>

<style>
html {
  height: 100%;
}
body {
  min-height: 100%;
}
</style>
