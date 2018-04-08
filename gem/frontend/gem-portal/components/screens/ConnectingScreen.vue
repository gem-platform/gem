<template>
  <GlobalMessage
    :title="title"
    :message="message"
    :class="type"/>
</template>

<script>
import GlobalMessage from '../GlobalMessage.vue';

export default {
  name: 'ConnectingScreen',
  components: {
    GlobalMessage
  },
  computed: {
    title() {
      const connection = this.$store.getters['meeting/connection/connection'];
      const handshake = this.$store.getters['meeting/connection/handshake'];

      if (connection.success === false) {
        return 'Connection failed';
      }
      if (handshake.success === false) {
        return 'Handshake failed';
      }

      return 'Connecting';
    },
    message() {
      const connection = this.$store.getters['meeting/connection/connection'];
      const handshake = this.$store.getters['meeting/connection/handshake'];

      return (
        connection.message ||
        handshake.message ||
        'We are connecting you to session'
      );
    },
    type() {
      const connection = this.$store.getters['meeting/connection/connection'];
      const handshake = this.$store.getters['meeting/connection/handshake'];

      if (connection.success === false || handshake.success === false) {
        return 'is-danger';
      }

      return 'is-primary';
    }
  }
};
</script>
