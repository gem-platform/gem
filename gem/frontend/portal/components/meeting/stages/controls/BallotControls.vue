<template>
  <div>
    <!-- Managing block -->
    <div
      v-if="canManage"
      class="field">

      <!-- Secret ballot switch -->
      <b-field label="Secret mode">
        <b-switch
          v-model="isSecret"
          @input="changeSecret">
          Secret ballot
        </b-switch>
      </b-field>

      <!-- Ballot threshold -->
      <b-field
        v-if="showThreshold"
        label="Threshold">
        <b-select
          v-model="threshold"
          placeholder="Ballot threshold"
          expanded
          @input="changeThreshold">
          <option value="0.5">Majority</option>
          <option value="0.66">2/3</option>
          <option value="0.8">4/5</option>
          <option value="1">Unanimous</option>
        </b-select>
      </b-field>
    </div>

    <!-- Voting controls -->
    <div v-if="canVote && !finished">
      <transition
        name="fade"
        mode="out-in">

        <!-- Vote buttons -->
        <div
          v-if="!voteCommited"
          key="vote-buttons"
          class="field is-grouped is-grouped-centered">
          <a
            class="button control is-success is-expanded is-large"
            @click="vote('yes')">Yes</a>
          <a
            class="button control is-danger is-expanded is-large"
            @click="vote('no')">No</a>
          <a
            class="button control is-info is-expanded is-large"
            @click="vote('abstained')">Abstained</a>
        </div>

        <!-- Vote accepted -->
        <a
          v-else
          key="change-mind"
          class="button control is-expanded is-large is-fullwidth is-success"
          @click="changeMind">
          Accepted. Change mind.
        </a>
      </transition>
    </div>

    <div
      v-if="finished"
      class="has-text-danger has-text-centered">
      Ballot completed
    </div>

    <!-- No rights to vote -->
    <div
      v-if="!canVote"
      class="has-text-danger has-text-centered">
      You do not have the right to vote.
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import CommunicationMixin from '@/components/CommunicationMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'BallotStageControls',
  mixins: [AuthMixin, NotificationMixin, CommunicationMixin, StageStateMixin],
  data() {
    return {
      voteCommited: false,
      isSecret: this.$store.getters['meeting/stage/state'].secret,
      threshold: this.$store.getters['meeting/stage/state'].threshold
    };
  },
  computed: {
    finished() {
      return this.$stage.finished;
    },

    /**
     * Can user vote?
     */
    canVote() {
      return this.haveAccess('meeting.vote');
    },

    /**
     * Can user manage ballot stage?
     */
    canManage() {
      return this.haveAccess('meeting.manage') && !this.finished;
    },

    /**
     * Show threshold dropdown?
     */
    showThreshold() {
      const { config } = this.$stage;
      return config ? !!config.enableThreshold : false;
    }
  },
  methods: {
    /**
     * Commit a vote
     */
    async vote(value) {
      try {
        await this.send('vote', { value });
        this.notify('Your vote has been accepted');
        this.voteCommited = true;
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Change mind
     */
    changeMind() {
      this.voteCommited = false;
    },

    /**
     * Set ballot secret value
     */
    async changeSecret(value) {
      try {
        await this.send('ballot_secret', { value });
        this.notify('Ballot secret state changed');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Set ballot threshold value
     */
    async changeThreshold(value) {
      try {
        await this.send('ballot_threshold', { value });
        this.notify('Ballot threshold changed');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    }
  }
};
</script>
