<template>
  <form>
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Request Quorum change</p>
      </header>

      <section class="modal-card-body">
        <b-message
          v-if="error"
          type="is-danger">
          {{ error }}
        </b-message>

        <b-message
          v-if="users.length == 0"
          type="is-danger">
          No one can approve quorum change.
        </b-message>

        <b-field label="Quorum value">
          <b-input
            v-model="value"
            size="is-large"
            placeholder="New quorum value" />
        </b-field>

        <b-field
          v-if="users && users.length > 0"
          label="Approval required from:">
          <div
            class="tags are-medium users-list">
            <b-tag
              v-for="user in users"
              :key="user._id"
              :class="{'is-success': isApprovedBy(user.id)}"
              rounded
              size="is-medium">
              {{ user.name }}
            </b-tag>
          </div>
        </b-field>
      </section>

      <footer class="modal-card-foot">
        <button
          class="button"
          type="button"
          @click="$parent.close()">
          Close
        </button>

        <button
          class="button is-primary"
          @click.prevent="requestQuorumChange">
          Request Change
        </button>
      </footer>
    </div>
  </form>
</template>

<script>
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  mixins: [CommunicationMixin],
  data() {
    const usersCanChange = this.$store.getters['meeting/quorum'].users_can_change;
    const usersStore = this.$store.getters['meeting/users'];

    return {
      value: 19,
      users: usersCanChange.map(x => usersStore[x]),
      approvedBy: [],
      error: undefined
    };
  },
  mounted() {
    this.$socket.on('quorum_change', this.quorumChange);
    this.$socket.on('vote_quorum_change', this.voteQuorumChange);
  },
  beforeDestroy() {
    this.$socket.off('quorum_change', this.quorumChange);
    this.$socket.off('vote_quorum_change', this.voteQuorumChange);
  },
  methods: {
    /**
     * Send a request to change a quorum.
     */
    async requestQuorumChange() {
      try {
        // Request a quorum change
        await this.request({
          command: 'request_quorum_change',
          data: { value: this.value }
        });
      } catch (e) {
        this.error = e.message;
      }
    },
    quorumChange(data) {
      if (data.stage === 'final' || data.stage === 'failed') {
        this.$parent.close();
      } else if (data.stage === 'progress') {
        this.approvedBy = data.approved_by;
      }
    },
    isApprovedBy(id) {
      return this.approvedBy.includes(id);
    }
  }
};
</script>

<style scoped>
.users-list {
  max-width: 350px;
}
</style>
