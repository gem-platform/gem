<template>
  <div>
    <MeetingScreenTopPanel
      :title="title"
      :subtitle="subtitle" />

    <section class="section">
      <div class="columns">
        <div class="column is-4">
          <div class="box">
            <ControlPanel/>
          </div>
          <div
            v-if="hasStageControls"
            class="box">
            <StageControlsPresenter/>
          </div>
        </div>

        <div class="column">
          <div
            v-if="hasStageView"
            class="box">
            <StageViewPresenter/>
          </div>

          <div
            v-if="hasProposal"
            class="box">
            {{ proposal.content }}
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import ControlPanel from '../ControlPanel.vue';
import StageViewPresenter from '../StageViewPresenter.vue';
import StageControlsPresenter from '../StageControlsPresenter.vue';
import MeetingScreenTopPanel from './MeetingScreenTopPanel.vue';

function humanReadableStageType(type) {
  return {
    ConnectedStage: 'Connected',
    AcquaintanceStage: 'Acquaintance',
    AgendaStage: 'Agenda',
    BallotStage: 'Ballot',
    BallotResultsStage: 'Ballot results',
    DiscussionStage: 'Discussion',
    CommentsStage: 'Comments',
  }[type] || type;
}

export default {
  name: 'MeetingScreen',
  components: {
    ControlPanel,
    StageViewPresenter,
    StageControlsPresenter,
    MeetingScreenTopPanel,
  },
  computed: {
    title() {
      const { meetingStageType, proposal } = this.$store.getters;

      return proposal ? proposal.title : humanReadableStageType(meetingStageType);
    },
    subtitle() {
      const type = this.$store.getters.meetingStageType;
      if (type === 'AgendaStage') { return ''; }
      if (type === 'ConnectedStage') { return ''; }
      return humanReadableStageType(type);
    },
    hasProposal() {
      return this.$store.getters.proposal !== undefined;
    },
    proposal() {
      return this.$store.getters.proposal;
    },
    hasStageControls() {
      const type = this.$store.getters.meetingStageType;
      return ['AcquaintanceStage', 'BallotStage', 'CommentsStage', 'DiscussionStage'].includes(type);
    },
    hasStageView() {
      const type = this.$store.getters.meetingStageType;
      return ['AgendaStage', 'BallotStage',
        'BallotResultsStage', 'CommentsStage', 'DiscussionStage'].includes(type);
    },
  },
};
</script>

<style scoped>
.footer-control {
   position: absolute;
   bottom: 0px;
   width: 100%;
   background: #d4d4d4;
}
</style>
