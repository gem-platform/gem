export default {
  computed: {
    $stage() {
      return this.$store.getters['meeting/stage/state'];
    },
    stageProposal() {
      return this.$store.getters['meeting/stage/proposal'];
    },
    stageType() {
      return this.$store.getters['meeting/stage/type'];
    }
  }
};

