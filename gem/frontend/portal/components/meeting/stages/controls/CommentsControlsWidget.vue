<template>
  <div class="speech-bubble">
    <!-- Textarea -->
    <div
      class="field">
      <textarea
        v-model="message"
        class="textarea is-dark"
        placeholder="Write your comment here"/>
    </div>

    <!-- Mark -->
    <div class="field is-grouped">
      <div class="select control is-small is-dark">
        <select v-model="mark">
          <option value="+">Plus</option>
          <option value="-">Minus</option>
          <option value="i">Info</option>
        </select>
      </div>

      <!-- Send comment -->
      <button
        class="button control is-expanded is-small is-dark"
        @click="sendComment">Send</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommentsStageControlsWidget',
  data() {
    return {
      message: '',
      mark: '+',
      quote: undefined
    };
  },
  methods: {
    /**
     * Send a comment
     */
    async sendComment() {
      this.$emit('comment', {
        message: this.message,
        mark: this.mark
      });
    }
  }
};
</script>
