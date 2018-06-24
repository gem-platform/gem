<template>
  <div>
    <!-- Managing block -->
    <div
      v-if="canManage"
      class="field">

      <!-- Secret ballot switch -->
      <b-switch
        v-model="isSecret"
        @input="changeSecret">
        Secret ballot
      </b-switch>
    </div>

    <!-- Voting controls -->
    <div v-if="canVote">
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

    <!-- No rights to vote -->
    <div
      v-else
      class="has-text-danger has-text-centered">
      You do not have the right to vote.
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'BallotStageControls',
  mixins: [AuthMixin, NotificationMixin, CommunicationMixin],
  data() {
    return {
      voteCommited: false,
      isSecret: this.$store.getters['meeting/stage/state'].secret
    };
  },
  computed: {
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
      return this.haveAccess('meeting.manage');
    }
  },
  methods: {
    /**
     * Commit a vote
     */
    async vote(value) {
      const res = await this.send('vote', { value });
      if (res.success) {
        this.notify('Your vote has been accepted');
        this.voteCommited = true;
      } else {
        this.notify(res.message, 'is-danger');
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
      this.isSecret = value;
      const res = await this.send('ballot_secret', { value });
      if (res.success) {
        this.notify('Ballot secret state changed');
      } else {
        this.notify(res.message, 'is-danger');
      }
    }
  }
};
</script>
