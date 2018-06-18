<template>
  <div>
    <div v-if="canComment">
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
          @click="send">Send</button>
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
import com from '@/lib/communication';
import AuthMixin from '@/components/AuthMixin';

export default {
  name: 'CommentsStageControls',
  mixins: [AuthMixin],
  data() {
    return {
      message: '',
      mark: '+'
    };
  },
  computed: {
    canComment() {
      return this.haveAccess('meeting.comment');
    }
  },
  methods: {
    send() {
      const { message, mark } = this;
      com
        .send('comment', { message, mark })
        .then(() => this.notify('Your comment has been accepted'))
        .catch(err => this.notify(err.message || 'err', 'is-danger'));
      this.message = '';
    },
    notify(message, type) {
      this.$bus.emit('notification', { message, type: type || 'is-success' });
    }
  }
};
</script>
