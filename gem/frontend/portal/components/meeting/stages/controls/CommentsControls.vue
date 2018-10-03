<template>
  <div>
    <div v-if="canComment">
      <!-- Quote -->
      <b-message
        :active="quote !== undefined"
        title="Quote"
        @close="quote = undefined">
        {{ quote ? quote.text : '' }}
      </b-message>

      <!-- Textarea -->
      <div
        class="field">
        <textarea
          v-model="message"
          class="textarea"
          placeholder="Write your comment here"/>
      </div>

      <!-- Mark -->
      <div class="field is-grouped">
        <div class="select control">
          <select v-model="mark">
            <option value="+">Plus</option>
            <option value="-">Minus</option>
            <option value="i">Info</option>
          </select>
        </div>

        <!-- Send comment -->
        <button
          class="button control is-expanded"
          @click="sendComment">Send</button>
      </div>
    </div>

    <!-- Have no rights -->
    <div
      v-else
      class="has-text-danger has-text-centered">
      You have no rights to comment.
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'CommentsStageControls',
  mixins: [AuthMixin, NotificationMixin, CommunicationMixin],
  data() {
    return {
      message: '',
      mark: '+',
      quote: undefined
    };
  },
  computed: {
    /**
     * Can user comment or not?
     */
    canComment() {
      return this.haveAccess('meeting.comment');
    }
  },
  mounted() {
    this.$bus.on('proposalSelection', this.onProposalSelection);
  },
  beforeDestroy() {
    this.$bus.off('proposalSelection', this.onProposalSelection);
  },
  methods: {
    /**
     * Send a comment
     */
    async sendComment() {
      const { message, mark } = this;

      // validate message
      if (!message) {
        this.notify('Message can not be empty.', 'is-danger');
        return;
      }

      // send message
      try {
        await this.send('comment', { message, mark, quote: this.quote });
        this.notify('Your comment has been accepted');
        this.message = '';
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * User selected something in proposal
     */
    onProposalSelection(data) {
      this.quote = data;
    }
  }
};
</script>
