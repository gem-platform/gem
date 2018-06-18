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
      <!-- Vote buttons -->
      <div
        v-if="!voteCommited"
        class="field is-grouped is-grouped-centered">
        <a
          class="button  control is-success is-expanded"
          @click="vote('yes')">Yes</a>
        <a
          class="button control is-danger is-expanded"
          @click="vote('no')">No</a>
        <a
          class="button control is-info is-expanded"
          @click="vote('abstained')">Abstained</a>
      </div>

      <!-- Vote accepted -->
      <a
        v-else
        class="button control is-expanded is-fullwidth is-success"
        @click="changeMind">
        Accepted. Change mind.
      </a>
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
import com from '@/lib/communication';
import AuthMixin from '@/components/AuthMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import NotificationMixin from '@/components/NotificationMixin';

export default {
  name: 'BallotStageControls',
  mixins: [AuthMixin, StageStateMixin, NotificationMixin],
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
      const res = await com.send('vote', { value });
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
      const res = await com.send('ballot_secret', { value });
      if (res.success) {
        this.notify('Ballot secret state changed');
      } else {
        this.notify(res.message, 'is-danger');
      }
    }
  }
};
</script>
