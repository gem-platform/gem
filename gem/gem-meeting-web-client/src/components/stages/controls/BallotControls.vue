<template>
  <div>
    <div v-if="canVote">
      <div
        v-if="voteCommited"
        class="field">
        <p class="control is-expanded">
          <a
            class="button is-fullwidth is-light"
            @click="changeMind">
            Accepted. Change mind.
          </a>
        </p>
      </div>

      <div
        v-else
        class="field is-grouped is-grouped-multiline is-grouped-centered">
        <p class="control is-expanded">
          <a
            class="button is-success is-fullwidth"
            @click="vote('yes')">Yes</a>
        </p>
        <p class="control is-expanded">
          <a
            class="button is-danger is-fullwidth"
            @click="vote('no')">No</a>
        </p>
        <p class="control is-expanded">
          <a
            class="button is-info is-fullwidth"
            @click="vote('abstained')">Abstained</a>
        </p>
      </div>
    </div>
    <div
      v-else
      class="has-text-danger has-text-centered">
      You do not have the right to vote.
    </div>
  </div>
</template>

<script>
import com from '@/communication';

export default {
  name: 'BallotStageControls',
  data() {
    return {
      voteCommited: false
    };
  },
  computed: {
    canVote() {
      const { user } = this.$store.getters;
      const permissions = user.permissions || [];
      return permissions.includes('vote');
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
    notify(message, type) {
      this.$bus.emit('notification', { message, type: type || 'is-success' });
    }
  }
};
</script>
