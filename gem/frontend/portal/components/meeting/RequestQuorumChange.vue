<template>
  <form>
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Request Quorum change</p>
      </header>

      <section class="modal-card-body">
        <b-field label="Quorum value">
          <b-input
            v-model="value"
            size="is-large"
            placeholder="New quorum value" />
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
import NotificationMixin from '@/components/NotificationMixin';

export default {
  mixins: [CommunicationMixin, NotificationMixin],
  data() {
    return {
      value: 19
    };
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

        this.$parent.close();
      } catch (e) {
        this.notify(e.message, 'is-danger');
      }
    }
  }
};
</script>
