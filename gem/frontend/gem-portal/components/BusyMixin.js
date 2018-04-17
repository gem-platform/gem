export default {
  computed: {
    busy() {
      return this.$store.getters.busy;
    }
  }
};
