<template>
  <div>
    <p class="heading has-text-centered">
      Ballot progress
    </p>

    <progress
      :value="progress"
      class="progress is-primary is-large"
      max="100"/>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'BallotStageView',
  mixins: [StageStateMixin],
  computed: {
    progress() {
      return this.$stage.finished
        ? 100
        : this.$stage.progress;
    }
  }
};
</script>
