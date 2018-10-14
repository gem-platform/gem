<template>
  <div>
    {{ message }}
    <!-- Commenting popup -->
    <div
      v-show="showCommentingPopup"
      id="test"
      ref="commentsPopup"
      class="commenting-popup">
      <CommentsControlWidget
        @comment="onWidgetComment"/>
    </div>

    <div v-if="canComment">
      <!-- Quote -->
      <b-message
        :active="showQuote"
        title="Quote"
        @close="quote = undefined">
        {{ quote ? quote.text : '' | truncate(256) }}
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
          @click="onButtonSendComment">Send</button>
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

import CommentsControlWidget from '@/components/meeting/stages/controls/CommentsControlsWidget.vue';

export default {
  name: 'CommentsStageControls',
  components: {
    CommentsControlWidget
  },
  mixins: [AuthMixin, NotificationMixin, CommunicationMixin],
  data() {
    return {
      message: '',
      mark: '+',
      quote: undefined,
      showCommentingPopup: false
    };
  },
  computed: {
    /**
     * Can user comment or not?
     */
    canComment() {
      return this.haveAccess('meeting.comment');
    },

    /**
     * Show quote block or not?
     */
    showQuote() {
      return this.quote
        ? this.quote.text !== undefined && this.quote.text !== ''
        : false;
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
    async sendComment(data) {
      const { message, mark, quote } = data;

      // validate message
      if (!message) {
        this.notify('Message can not be empty.', 'is-danger');
        return;
      }

      // send message
      try {
        await this.send('comment', { message, mark, quote });
        this.notify('Your comment has been accepted');
        this.message = '';
        this.quote = undefined;
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    onButtonSendComment() {
      this.sendComment({
        message: this.message,
        mark: this.mark,
        quote: this.quote
      });
    },

    onWidgetComment(data) {
      this.sendComment({
        message: data.message,
        mark: data.mark,
        quote: this.quote
      });
      this.showCommentingPopup = false;
    },

    /**
     * User selected something in proposal
     */
    onProposalSelection(data) {
      this.showCommentingPopup = !!data.text;

      if (data.text) {
        let left = document.body.clientWidth - (data.event.pageX + 200);
        left = Math.min(0, left);

        this.quote = { text: data.text, begin: data.begin, end: data.end };
        this.$refs.commentsPopup.style.left = `${data.event.pageX + left}px`;
        this.$refs.commentsPopup.style.top = `${data.event.pageY}px`;
      }
    }
  }
};
</script>

<style scoped>
.commenting-popup {
  position: absolute;
  min-width: 200px;
  min-height: 100px;
  background-color: white;
  border: 1px solid hsl(0, 0%, 86%);
  box-shadow: 2px 2px 2px rgba(0,0,0,.5);
  padding: 10px;
  border-radius: 5px;
}
</style>
