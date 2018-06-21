<template>
  <div>
    <!-- Top panel -->
    <MeetingScreenTopPanel
      :title="title"
      :subtitle="subtitle" />

    <!-- Stage controls and view -->
    <div class="columns">
      <!-- Stage controls -->
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

      <div class="column is-8">
        <!-- Stage view -->
        <div
          v-if="showStageView"
          class="box">
          <StageViewPresenter/>
        </div>

        <!-- Stage proposal -->
        <div
          v-if="showProposal"
          class="box content">
          <div v-html="proposal.content"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ControlPanel from '@/components/meeting/ControlPanel.vue';
import StageViewPresenter from '@/components/meeting/StageViewPresenter.vue';
import StageControlsPresenter from '@/components/meeting/StageControlsPresenter.vue';
import MeetingScreenTopPanel from '@/components/meeting/MeetingScreenTopPanel.vue';
import StageMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'MeetingScreen',
  components: {
    ControlPanel,
    StageViewPresenter,
    StageControlsPresenter,
    MeetingScreenTopPanel
  },
  mixins: [StageMixin],
  computed: {
    /**
     * Title for top panel
     */
    title() {
      return this.stageProposal
        ? this.stageProposal.title
        : this.stageConfig.title;
    },

    /**
     * Subtitle for top panel
     */
    subtitle() {
      return this.stageConfig.type === true ? this.stageConfig.title : '';
    },

    /**
     * Proposal for current stage
     */
    proposal() {
      return this.stageProposal;
    },

    /**
     * Show proposal or not?
     */
    showProposal() {
      return this.stageProposal !== undefined;
    },

    /**
     * Show stage controls or not?
     */
    showStageControls() {
      return this.stageConfig.controls === true;
    },

    /**
     * Show stage view or not?
     */
    showStageView() {
      return this.stageConfig.view === true;
    },

    /**
     * Show global contol panel or not?
     */
    showControlPanel() {
      return this.$store.getters['meeting/user'].hasPermission('session:manage');
    },

    /**
     * Return configuration of stage
     */
    stageConfig() {
      const type = this.stageType;
      const stages = {
        ConnectedStage: { title: 'Connected' },
        AgendaStage: { title: 'Agenda', view: true },
        AcquaintanceStage: {
          title: 'Acquaintance', controls: true, type: true
        },
        BallotStage: {
          title: 'Ballot', controls: true, view: true, type: true
        },
        BallotResultsStage: {
          title: 'Ballot results', view: true, type: true
        },
        DiscussionStage: {
          title: 'Discussion', controls: true, view: true, type: true
        },
        CommentsStage: {
          title: 'Comments', controls: true, view: true, type: true
        },
        FinalStage: {
          title: 'Final', controls: true, view: true
        }
      };
      return stages[type];
    }
  }
};
</script>
