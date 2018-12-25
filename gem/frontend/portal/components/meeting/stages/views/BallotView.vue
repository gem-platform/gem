<template>
  <div>
    <!-- Quorum is not met message -->
    <b-message
      v-if="!isQuorumMet"
      size="is-large"
      type="is-danger">
      Quorum is not met. {{ usersOnlineCount }} of {{ quorumValue }} are present.
    </b-message>

    <!-- Ballot progress -->
    <div
      v-if="isQuorumMet">

      <p class="heading has-text-centered">
        Ballot progress
      </p>

      <progress
        :value="progress"
        class="progress is-primary is-large"
        max="100"/>
    </div>
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
    },
    isQuorumMet() {
      return this.$stage.isQuorumMet;
    },
    quorumValue() {
      return this.$store.getters['meeting/quorum'].value;
    },
    usersOnlineCount() {
      const { usersOnline } = this.$store.state.meeting;
      return usersOnline.online.length;
    }
  }
};
</script>
