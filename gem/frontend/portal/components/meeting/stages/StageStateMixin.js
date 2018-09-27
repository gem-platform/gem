export default {
  computed: {
    $stage() {
      return this.$store.getters['meeting/stage/state'];
    },
    stageIndex() {
      return this.$store.getters['meeting/stage/index'];
    },
    stagesCount() {
      return Object.keys(this.$store.state.meeting.stages).length;
    },
    stageProposal() {
      return this.$store.getters['meeting/stage/proposal'];
    },
    stageType() {
      return this.$store.getters['meeting/stage/type'];
    },
    meetingTime() {
      return { start: this.$store.state.meeting.start, end: this.$store.state.meeting.end };
    },
    proposals() {
      return Object.values(this.$store.getters['meeting/proposals']);
    }
  },
  methods: {
    setStageTimer(seconds) {
      const now = new Date();
      const ahead = new Date(now.getTime() + (1000 * seconds));
      this.$bus.emit('setStageTimer', ahead);
    }
  }
};

