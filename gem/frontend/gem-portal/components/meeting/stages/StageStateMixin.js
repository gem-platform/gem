export default {
  computed: {
    $stage() {
      return this.$store.getters['meeting/stage/state'];
    }
  }
};

