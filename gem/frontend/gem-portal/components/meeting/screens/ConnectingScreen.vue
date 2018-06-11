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
    title() {
      const connection = this.$store.getters['meeting/connection/state'];
      return connection.state;
    },
    message() {
      const connection = this.$store.getters['meeting/connection/state'];
      return connection.message || 'We are connecting you to session';
    },
    type() {
      const connection = this.$store.getters['meeting/connection/state'];
      return connection.state === 'disconnected' ? 'is-danger' : 'is-white';
    }
  }
};
</script>
