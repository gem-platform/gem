<template>
  <form>
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Quick ballot</p>
      </header>

      <section class="modal-card-body">
        <b-field label="Question">
          <b-input
            v-model="question"
            size="is-large"
            placeholder="Question" />
        </b-field>

        <label class="label">Options</label>
        <b-field
          v-for="(option, idx) in options"
          :key="idx">
          <b-input
            v-model="options[idx]"
            :placeholder="'Option ' + (idx + 1)" />
        </b-field>
      </section>

      <footer class="modal-card-foot">
        <button
          class="button"
          type="button"
          @click="addOption">
          Add option
        </button>

        <button
          class="button"
          type="button"
          @click="$parent.close()">
          Close
        </button>

        <button
          class="button is-primary"
          @click.prevent="create">
          Create
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
      options: ['', ''],
      question: ''
    };
  },
  methods: {
    /**
     * Create quick ballot.
     */
    async create() {
      try {
        // Request a new Quick Ballot.
        await this.request({
          command: 'request_quick_ballot',
          data: {
            question: this.question,
            options: this.options
          }
        });

        // New Quick Baloot has been requested. So close dialog,
        this.$parent.close();
      } catch (e) {
        this.notify(e.message, 'is-danger');
      }
    },

    /**
     * Add new option to the end of list.
     */
    addOption() {
      this.options.push(undefined);
    }
  }
};
</script>
