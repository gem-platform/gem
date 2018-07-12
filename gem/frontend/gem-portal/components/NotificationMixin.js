export default {
  methods: {
    notify(message, type) {
      this.$snackbar.open({ message, type: type || 'is-success', queue: false });
    }
  }
};
