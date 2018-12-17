<template>
  <form>
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ question }}</p>
      </header>

      <section class="modal-card-body">
        <!-- Overall progress -->
        <progress
          v-if="!isBallotCompleted"
          :value="votesCount"
          :max="onlineCount"
          class="progress is-primary is-large"/>

        <!-- Options -->
        <b-field
          v-for="(option, idx) in options"
          :key="idx">

          <button
            :disabled="isVoteCommited"
            :class="{'is-outlined': voteCommited != idx}"
            class="button is-fullwidth is-primary"
            @click.prevent="vote(idx)">
            {{ option }}
            <span v-if="isVoteCommited">
              &nbsp;
              ({{ (results[idx] || 0) / onlineCount * 100 }}% /
              {{ results[idx] || 0 }} votes)
            </span>
          </button>
        </b-field>

        <!-- Close -->
        <button
          v-if="isBallotCompleted"
          class="button is-fullwidth is-danger"
          @click.prevent="close">
          Close
        </button>
      </section>
    </div>
  </form>
</template>

<script>
import CommunicationMixin from '@/components/CommunicationMixin';
import NotificationMixin from '@/components/NotificationMixin';

export default {
  mixins: [CommunicationMixin, NotificationMixin],
  props: {
    question: {
      type: String,
      required: true
    },
    options: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      isVoteCommited: false,
      voteCommited: undefined,
      results: {},
      onlineCount: 0
    };
  },
  computed: {
    /**
     * Get count of commited votes.
     */
    votesCount() {
      return Object
        .values(this.results)
        .reduce((sum, value) => sum + value, 0);
    },

    /**
     * Baloot is bompleted if anyone had commited his vote.
     */
    isBallotCompleted() {
      return this.votesCount >= this.onlineCount
        && this.onlineCount > 0;
    }
  },
  mounted() {
    this.$socket.on('quick_ballot_results', this.quickBallotResults);
  },
  beforeDestroy() {
    this.$socket.off('quick_ballot_results', this.quickBallotResults);
  },
  methods: {
    /**
     * Commit a vote.
     */
    async vote(idx) {
      try {
        await this.request({
          command: 'quick_ballot_vote',
          data: { vote: idx }
        });
        this.isVoteCommited = true;
        this.voteCommited = idx;
      } catch (e) {
        this.notify(e.message, 'is-danger');
      }
    },

    /**
     * Quick ballot results receied.
     */
    quickBallotResults(data) {
      this.results = data.results;
      this.onlineCount = data.online_count;
    },

    /**
     * Close dialog.
     */
    close() {
      this.$parent.close();
    }
  }
};
</script>
