<template>
  <form>
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Quorum change</p>
      </header>

      <section class="modal-card-body">
        <b-field label="Quorum value">
          New quorum value: {{ value }}.
        </b-field>
      </section>

      <footer class="modal-card-foot">
        <button
          class="button is-success"
          type="button"
          @click.prevent="vote(true)">
          Accept
        </button>

        <button
          class="button is-danger"
          type="button"
          @click.prevent="vote(false)">
          Reject
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
  props: {
    value: {
      type: Number,
      required: true
    }
  },
  methods: {
    /**
     * Send a request to change a quorum.
     */
    async vote(value) {
      try {
        // Request a quorum change
        await this.request({
          command: 'vote_quorum_change',
          data: { value }
        });

        this.$parent.close();
      } catch (e) {
        this.notify(e.message, 'is-danger');
      }
    }
  }
};
</script>
