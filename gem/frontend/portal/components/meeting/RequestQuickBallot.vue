<template>
  <form action="">
    <div
      class="modal-card"
      style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Quick ballot</p>
      </header>

      <section class="modal-card-body">
        <b-field
          v-for="(option, idx) in options"
          :key="option">
          <b-input
            :value="option"
            :placeholder="'Option ' + idx" />
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
      options: [undefined, undefined]
    };
  },
  methods: {
    /**
     * Create quick ballot.
     */
    async create() {
      try {
        await this.request({ command: 'quick_ballot', data: this.options });
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
