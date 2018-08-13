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
        <!-- Additional stage widgets -->
        <div
          v-for="(widget, index) in widgets"
          :key="index"
          class="box">
          <component :is="widget"/>
        </div>

        <!-- Stage proposal -->
        <div
          v-if="showProposal"
          class="box content">
          <ProposalReader
            v-if="showProposalReader"/>
          <div
            v-else
            v-html="proposal.content"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProposalReader from '@/components/meeting/ProposalReader.vue';
import ControlPanel from '@/components/meeting/ControlPanel.vue';
import StageViewPresenter from '@/components/meeting/StageViewPresenter.vue';
import StageControlsPresenter from '@/components/meeting/StageControlsPresenter.vue';
import StageInfo from '@/components/meeting/stages/StageInfo.vue';
import UsersOnline from '@/components/meeting/UsersOnline.vue';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import UserInactiveMixin from '@/components/meeting/screens/UserInactiveMixin';

// view components

import AgendaView from '@/components/meeting/stages/views/AgendaView.vue';
import AcquaintanceView from '@/components/meeting/stages/views/AcquaintanceView.vue';
import BallotView from '@/components/meeting/stages/views/BallotView.vue';
import BallotResultsView from '@/components/meeting/stages/views/BallotResultsView.vue';
import CommentsView from '@/components/meeting/stages/views/CommentsView.vue';
import DiscussionView from '@/components/meeting/stages/views/DiscussionView.vue';
import FinalView from '@/components/meeting/stages/views/FinalView.vue';

// view vidgets

import CommentsList from '@/components/meeting/stages/widgets/CommentsList.vue';
import BallotResults from '@/components/meeting/stages/widgets/BallotResults.vue';


export default {
  name: 'MeetingScreen',
  components: {
    ProposalReader,
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
     * Show proposal reader or content?
     */
    showProposalReader() {
      return this.stageConfig.proposalReader === true;
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

    widgets() {
      return this.stageConfig.widgets;
    },

    /**
     * Return configuration of stage
     */
    stageConfig() {
      const type = this.stageType;
      const stages = {
        ConnectedStage: {
          title: 'Connected'
        },
        AgendaStage: {
          title: 'Agenda',
          widgets: [
            AgendaView
          ]
        },
        AcquaintanceStage: {
          title: 'Acquaintance',
          controls: false,
          type: true,
          proposalReader: true,
          widgets: [
            AcquaintanceView,
            BallotResults,
            CommentsList
          ]
        },
        BallotStage: {
          title: 'Ballot',
          controls: true,
          type: true,
          widgets: [
            BallotView
          ]
        },
        BallotResultsStage: {
          title: 'Ballot results',
          type: true,
          widgets: [
            BallotResultsView
          ]
        },
        DiscussionStage: {
          title: 'Discussion',
          controls: true,
          type: true,
          widgets: [
            DiscussionView
          ]
        },
        CommentsStage: {
          title: 'Comments',
          controls: true,
          type: true,
          widgets: [
            CommentsView
          ]
        },
        FinalStage: {
          title: 'Final',
          controls: true,
          widgets: [
            FinalView
          ]
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
      if (!this.closed) { return; }
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
