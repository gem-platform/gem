<template>
  <div>
    <transition name="fade">
      <div
        v-if="next"
        class="field">
        <p class="heading has-text-centered">Next stage</p>
        <div
          :class="{'is-success': next.differentProposal, 'is-danger': next.final}"
          class="notification has-text-centered next">
          <p v-if="next.differentProposal && !next.final">
            <strong>{{ next.nextProposal }}</strong>
          </p>
          <p v-else>
            {{ next.type | stageType }}
          </p>
        </div>
      </div>
    </transition>

    <p class="heading has-text-centered">Change meeting stage</p>
    <div class="field is-grouped is-grouped-multiline">
      <!-- "Previous stage" button -->
      <p class="control">
        <button
          id="prev"
          :disabled="prevDisabled"
          class="button"
          @click="move(-1)">Prev</button>
      </p>

      <!-- "Next stage" button -->
      <p class="control is-expanded">
        <button
          id="next"
          :disabled="nextDisabled"
          class="button is-fullwidth"
          @click="move(1)">
          <span>Next</span>
          <span class="icon">
            <i class="fa fa-angle-right"/>
          </span>
        </button>
      </p>
    </div>

    <p class="heading has-text-centered">Stage timer</p>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <a
          class="button"
          @click="switchTimerMode">{{ timerMode }}</a>
      </p>
      <p class="control">
        <a
          class="button"
          @click="setStageTime(60, timerMode)">1 min</a>
      </p>
      <p class="control is-expanded">
        <a
          class="button is-fullwidth"
          @click="setStageTime(120, timerMode)">2 min</a>
      </p>
      <p class="control">
        <a
          class="button"
          @click="setStageTime(180, timerMode)">3 min</a>
      </p>
      <p class="control">
        <a
          class="button"
          @click="setStageTime(300, timerMode)">5 min</a>
      </p>
    </div>

    <p class="heading has-text-centered">Utils</p>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control is-expanded">
        <button
          class="button is-fullwidth"
          @click="requestQuickBallot">Quick ballot</button>
      </p>
    </div>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import RequestQuickBallot from '@/components/meeting/RequestQuickBallot.vue';
import NotificationMixin from '@/components/NotificationMixin';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'ControlPanel',
  filters: {
    stageType(value) {
      const words = value.split(/(?=[A-Z])/);
      words.pop();
      return words.join(' ');
    }
  },
  mixins: [StageStateMixin, NotificationMixin, CommunicationMixin],
  data() {
    return {
      timerMode: '+'
    };
  },
  computed: {
    /**
     * Disable "Next" button or not?
     */
    nextDisabled() {
      return this.stageIndex >= this.stagesCount - 1;
    },

    /**
     * Disable "Prev" button or not?
     */
    prevDisabled() {
      return this.stageIndex <= 0;
    },

    /**
     * Returns next stage data
     */
    next() {
      const { stages, proposals } = this.$store.state.meeting;

      // get next stage of the meeting
      const stage = stages[this.stageIndex + 1];
      if (!stage) { return undefined; }

      // get proposal data
      const proposal = proposals[stage.proposalId];
      const nextProposal = proposal ? proposal.title : '';
      const currentProposal = this.stageProposal ? this.stageProposal.title : '';
      return {
        type: stage.type,
        nextProposal,
        currentProposal,
        differentProposal: nextProposal !== currentProposal,
        final: stage.type === 'FinalStage'
      };
    }
  },
  methods: {
    /**
     * Move to next stage
     */
    async move(step) {
      const nextStageIndex = this.stageIndex + step;
      try {
        await this.send('switch_stage', { index: nextStageIndex });
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Switch timer mode
     */
    switchTimerMode() {
      this.timerMode = this.timerMode === '+' ? '=' : '+';
    },

    /**
     * Add stage time using specified seconds
     */
    async setStageTime(seconds, mode) {
      try {
        await this.send('stage_timer', { value: seconds, mode });
        this.notify('Time has been successfully updated');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Open dialog to create a new Quick Ballot.
     */
    requestQuickBallot() {
      this.$modal.open({
        parent: this,
        component: RequestQuickBallot,
        hasModalCard: true
      });
    }
  }
};
</script>

<style scoped>
.next {
  transition: background-color 0.5s ease;
}
</style>
