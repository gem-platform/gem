<template>
  <div id="app">
    <transition
      name="fade"
      mode="out-in">
      <component :is="screen"/>
    </transition>
  </div>
</template>

<script>
import MeetingScreen from './components/screens/MeetingScreen.vue';
import ConnectingScreen from './components/screens/ConnectingScreen.vue';

export default {
  name: 'GemPlatform',
  components: {
    MeetingScreen,
    ConnectingScreen
  },
  computed: {
    screen() {
      const hs = this.$store.getters.handshake.success === true;
      return hs ? 'MeetingScreen' : 'ConnectingScreen';
    }
  },
  created() {
    this.$bus.on('notification', this.snackbar);
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
