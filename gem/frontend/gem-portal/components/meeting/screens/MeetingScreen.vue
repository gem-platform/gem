<template>
  <div>
    <!-- Top panel -->
    <StageInfo
      :title="title"
      :type="type" />

    <!-- Stage controls and view -->
    <div class="columns">
      <!-- Stage controls -->
      <div class="column is-4">
        <!-- -->
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

        <!-- Users online -->
        <div class="box">
          <UsersOnline/>
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
import StageInfo from '@/components/meeting/stages/StageInfo.vue';
import UsersOnline from '@/components/meeting/UsersOnline.vue';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import UserInactiveMixin from '@/components/meeting/screens/UserInactiveMixin';

export default {
  name: 'MeetingScreen',
  components: {
    ControlPanel,
    StageViewPresenter,
    StageControlsPresenter,
    StageInfo,
    UsersOnline
  },
  mixins: [StageStateMixin, UserInactiveMixin],
  computed: {
    /**
     * Title for top panel
     */
    title() {
      return this.proposal
        ? this.proposal.title
        : this.stageConfig.title;
    },

    /**
     * Subtitle for top panel
     */
    type() {
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
      return this.$store.getters['meeting/user'].hasPermission('meeting.manage');
    },

    /**
     * Is meeting closed or not?
     */
    closed() {
      return this.$store.state.meeting.closed;
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
          title: 'Acquaintance', controls: true, view: true, type: true
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
  },
  watch: {
    /**
     * Stage changed
     */
    stageIndex() {
      // set stage timer on stage change
      this.setStageTimer(120);
    },

    /**
     * Meeting is closed
     */
    closed() {
      const { $router, $store } = this;

      this.$dialog.alert({
        title: 'Meeting is closed',
        canCancel: false,
        message: 'You will be redirected to Schedule page',
        type: 'is-success',
        hasIcon: true,
        icon: 'check-circle',
        iconPack: 'fa',
        onConfirm() {
          // redirect user to home page
          $router.push('/');

          // user is no more connected to meeting, so
          // hide "meeting" tab from NavBar
          $store.dispatch('meeting/meetingId', 0);
        }
      });
    }
  },
  mounted() {
    this.setStageTimer(120);
  }
};
</script>
