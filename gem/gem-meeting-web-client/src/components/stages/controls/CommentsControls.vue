<template>
  <div>
    <div class="field">
      <textarea
        v-model="message"
        class="textarea"
        placeholder="Write your comment here"/>
    </div>

    <div class="field is-grouped">
      <div class="select control">
        <select v-model="mark">
          <option value="+">Plus</option>
          <option value="-">Minus</option>
          <option value="i">Info</option>
        </select>
      </div>

      <button
        class="button control is-expanded"
        @click="send">Send</button>
    </div>

  </div>
</template>

<script>
import com from '@/communication';

export default {
  name: 'CommentsStageControls',
  data() {
    return {
      message: '',
      mark: '+'
    };
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
