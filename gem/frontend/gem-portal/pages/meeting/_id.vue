<template>
  <no-ssr>
    <component :is="screen"/>
  </no-ssr>
</template>

<script>
import MeetingScreen from '@/components/meeting/screens/MeetingScreen.vue';
import ConnectingScreen from '@/components/meeting/screens/ConnectingScreen.vue';
import MeetingSocketHandlersMixin from '@/components/meeting/screens/MeetingSocketHandlersMixin';

export default {
  name: 'GemPlatform',
  layout: 'portal',
  components: {
    MeetingScreen,
    ConnectingScreen
  },
  mixins: [MeetingSocketHandlersMixin],
  computed: {
    screen() {
      const hs = this.$store.getters['meeting/connection/state'].state === 'connected';
      return hs ? 'MeetingScreen' : 'ConnectingScreen';
    }
  }
};
</script>
