<template>
  <div>
    <MeetingScreenTopPanel
      :title="title"
      :subtitle="subtitle" />

    <section class="section">
      <div class="columns">
        <div class="column is-4">
          <div
            v-if="showControlPanel"
            class="box">
            <ControlPanel/>
          </div>
          <div
            v-if="showStageControls"
            class="box">
            <StageControlsPresenter/>
          </div>
        </div>

        <div class="column">
          <div
            v-if="showStageView"
            class="box">
            <StageViewPresenter/>
          </div>

          <div
            v-if="showProposal"
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
  return (
    {
      ConnectedStage: 'Connected',
      AcquaintanceStage: 'Acquaintance',
      AgendaStage: 'Agenda',
      BallotStage: 'Ballot',
      BallotResultsStage: 'Ballot results',
      DiscussionStage: 'Discussion',
      CommentsStage: 'Comments'
    }[type] || type
  );
}

export default {
  name: 'MeetingScreen',
  components: {
    ControlPanel,
    StageViewPresenter,
    StageControlsPresenter,
    MeetingScreenTopPanel
  },
  computed: {
    title() {
      const meetingStageType = this.$store.getters['meeting/stageType'];
      const proposal = this.$store.getters['meeting/proposal'];

      return proposal
        ? proposal.title
        : humanReadableStageType(meetingStageType);
    },
    subtitle() {
      const type = this.$store.getters['meeting/stageType'];
      const withoutSubtitle = ['AgendaStage', 'ConnectedStage'];
      const showSubtitle = !withoutSubtitle.includes(type);
      return showSubtitle ? humanReadableStageType(type) : '';
    },
    proposal() {
      return this.$store.getters['meeting/proposal'];
    },
    showProposal() {
      return this.$store.getters['meeting/proposal'] !== undefined;
    },
    showStageControls() {
      const type = this.$store.getters['meeting/stageType'];
      const withControls = [
        'AcquaintanceStage',
        'BallotStage',
        'CommentsStage',
        'DiscussionStage'
      ];
      return withControls.includes(type);
    },
    showStageView() {
      const type = this.$store.getters['meeting/stageType'];
      const withViews = [
        'AgendaStage',
        'BallotStage',
        'BallotResultsStage',
        'CommentsStage',
        'DiscussionStage'
      ];
      return withViews.includes(type);
    },
    showControlPanel() {
      return this.$store.getters['meeting/user'].hasPermission(
        'session:manage'
      );
    }
  }
};
</script>
