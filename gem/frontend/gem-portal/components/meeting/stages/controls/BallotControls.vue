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

export default {
  name: 'BallotStageControls',
  mixins: [AuthMixin, StageStateMixin],
  data() {
    return {
      voteCommited: false,
      isSecret: this.$store.getters['meeting/stage/state'].secret
    };
  },
  computed: {
    canVote() {
      return this.haveAccess('meeting.vote');
    },
    canManage() {
      return this.haveAccess('meeting.manage');
    }
  },
  methods: {
    vote(value) {
      com
        .send('vote', { value })
        .then(() => {
          this.notify('Your vote has been accepted');
          this.voteCommited = true;
        })
        .catch(err => this.notify(err.message, 'is-danger'));
    },
    changeMind() {
      this.voteCommited = false;
    },
    async changeSecret(value) {
      this.isSecret = value;
      const res = await com.send('ballot_secret', { value });
      if (res.success) {
        this.notify('Ballot secret state changed');
      }
    },
    notify(message, type) {
      this.$bus.emit('notification', { message, type: type || 'is-success' });
    }
  }
};
</script>
