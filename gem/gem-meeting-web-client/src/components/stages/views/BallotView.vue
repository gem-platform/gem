<template>
  <div>
    <progress
      :value="progress"
      class="progress is-primary is-large"
      max="100">test</progress>
  </div>
</template>

<script>
export default {
  name: 'BallotStageView',
  computed: {
    progress() {
      return this.$store.getters.meetingStageState.progress;
    }
  }
};
</script>
