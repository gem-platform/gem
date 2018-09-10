<template>
  <GlobalMessage
    :title="title"
    :message="message"
    :class="type"/>
</template>

<script>
import GlobalMessage from '@/components/GlobalMessage.vue';

export default {
  name: 'ConnectingScreen',
  components: {
    GlobalMessage
  },
  computed: {
    /**
     * Returns connection state
     */
    connection() {
      return this.$store.state.meeting.connection;
    },

    /**
     * Title for connection screen
     */
    title() {
      return this.connection.state;
    },

    /**
     * Message for connection screen
     */
    message() {
      return this.connection.message || 'We are connecting you to session';
    },

    /**
     * Type of message
     */
    type() {
      return this.connection.state === 'disconnected' ? 'is-danger' : 'is-white';
    }
  }
};
</script>
