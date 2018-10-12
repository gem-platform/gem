<template>
  <div>
    <!-- Top panel -->
    <StageInfo
      :title="title"
      :type="type" />

    <!-- Stage controls and view -->
    <div class="columns">
      <!-- Stage controls -->
      <div
        v-if="!isPresenter"
        class="column is-4">

        <!-- -->
        <div
          v-if="showControlPanel"
          class="box">
          <ControlPanel/>
        </div>

        <!-- Additional controll widgets -->
        <div
          v-for="(control, index) in controls"
          :key="index"
          class="box">
          <component :is="control"/>
        </div>

        <!-- Users online -->
        <div class="box">
          <UsersOnline/>
        </div>
      </div>

      <div
        :class="{'is-8': !isPresenter}"
        class="column">
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
            :mode="proposalReaderMode"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// mixins

import AuthMixin from '@/components/AuthMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import UserInactiveMixin from '@/components/meeting/screens/UserInactiveMixin';

// components

import ProposalReader from '@/components/meeting/ProposalReader.vue';
import ControlPanel from '@/components/meeting/ControlPanel.vue';
import StageControlsPresenter from '@/components/meeting/StageControlsPresenter.vue';
import StageInfo from '@/components/meeting/stages/StageInfo.vue';
import UsersOnline from '@/components/meeting/UsersOnline.vue';

// view components

import AgendaView from '@/components/meeting/stages/views/AgendaView.vue';
import AcquaintanceView from '@/components/meeting/stages/views/AcquaintanceView.vue';
import BallotView from '@/components/meeting/stages/views/BallotView.vue';
import BallotResultsView from '@/components/meeting/stages/views/BallotResultsView.vue';
import CommentsView from '@/components/meeting/stages/views/CommentsView.vue';
import DiscussionView from '@/components/meeting/stages/views/DiscussionView.vue';
import FinalView from '@/components/meeting/stages/views/FinalView.vue';

// controlls components

import BallotControls from '@/components/meeting/stages/controls/BallotControls.vue';
import CommentsControls from '@/components/meeting/stages/controls/CommentsControls.vue';
import DiscussionControls from '@/components/meeting/stages/controls/DiscussionControls.vue';
import FinalControls from '@/components/meeting/stages/controls/FinalControls.vue';

// view vidgets

import CommentsList from '@/components/meeting/stages/widgets/CommentsList.vue';
import BallotResults from '@/components/meeting/stages/widgets/BallotResults.vue';


export default {
  name: 'MeetingScreen',
  components: {
    ProposalReader,
    ControlPanel,
    StageControlsPresenter,
    StageInfo,
    UsersOnline
  },
  mixins: [AuthMixin, StageStateMixin, UserInactiveMixin],
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
     * Show proposal reader or content?
     */
    proposalReaderMode() {
      const { config } = this.$stage;
      return this.isPresenter
        ? 'all' // show whole proposal if user is presenter
        : config.proposalDisplayMode || 'all';
    },

    /**
     * Show global contol panel or not?
     */
    showControlPanel() {
      return this.haveAccess('meeting.manage');
    },

    /**
     * Is user presenter?
     */
    isPresenter() {
      return this.haveScope('meeting.presenter');
    },

    /**
     * Is meeting closed or not?
     */
    closed() {
      return this.$store.state.meeting.closed;
    },

    controls() {
      return this.stageConfig.controls;
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
          controls: [],
          widgets: [
            AgendaView
          ]
        },
        AcquaintanceStage: {
          title: 'Acquaintance',
          type: true,
          controls: [],
          widgets: [
            AcquaintanceView,
            BallotResults,
            CommentsList
          ]
        },
        BallotStage: {
          title: 'Ballot',
          type: true,
          controls: [
            BallotControls
          ],
          widgets: [
            BallotView
          ]
        },
        BallotResultsStage: {
          title: 'Ballot results',
          type: true,
          controls: [],
          widgets: [
            BallotResultsView
          ]
        },
        DiscussionStage: {
          title: 'Discussion',
          type: true,
          controls: [
            DiscussionControls
          ],
          widgets: [
            DiscussionView
          ]
        },
        CommentsStage: {
          title: 'Comments',
          type: true,
          controls: [
            CommentsControls,
            CommentsView
          ]
        },
        FinalStage: {
          title: 'Final',
          controls: [
            FinalControls
          ],
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
      const { config } = this.$stage;
      const duration = ((config && config.duration) || 2) * 60;
      this.setStageTimer(duration);
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
