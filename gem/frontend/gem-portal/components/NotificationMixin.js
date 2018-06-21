export default {
  methods: {
    notify(message, type) {
      this.$bus.emit('notification', { message, type: type || 'is-success', queue: false });
    }
  }
};
