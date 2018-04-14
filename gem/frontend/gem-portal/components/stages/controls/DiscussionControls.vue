<template>
  <div>
    <div class="buttons is-centered">
      <a
        v-if="!selfInQueue"
        class="button"
        @click="requestFloor()">Request a floor</a>
      <a
        v-else
        class="button"
        @click="withdrawFromQueue()">Withdraw from queue</a>
    </div>

    <b-table
      :data="queue"
      :columns="columns">
      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            Queue is empty.
          </div>
        </section>
      </template>

      <template slot-scope="props">
        <b-table-column label="Name">
          {{ props.row.name }}
        </b-table-column>

        <b-table-column label="Actions">
          <b-tooltip
            label="Give a voice"
            position="is-left">
            <a
              class="button is-white is-small"
              @click="giveVoice(props.row.id)">V</a>
          </b-tooltip>

          <b-tooltip
            label="Remove from queue"
            position="is-left">
            <a
              class="button is-white is-small"
              @click="removeFromQueue(props.row.id)">R</a>
          </b-tooltip>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import com from '@/lib/communication';

export default {
  name: 'DiscussionStageControls',
  computed: {
    queue() {
      const queue = this.$store.getters['meeting/stage/state'].queue;
      const users = this.$store.getters['meeting/users'];
      return queue.map(x => users[x]);
    },
    speaker() {
      const queue = this.$store.getters['meeting/stage/state'].speaker;
      const users = this.$store.getters['meeting/users'];
      return users[speaker];
    },
    columns() {
      return [
        { field: 'name', label: 'Name' },
        { field: 'id', label: 'Actions', width: '100' }
      ];
    },
    selfInQueue() {
      const queue = this.$store.getters['meeting/stage/state'].queue;
      const user = this.$store.getters['meeting/user'];
      return queue.includes(user.id);
    }
  },
  created() {
    com.set(this.$socket);
  },
  methods: {
    requestFloor() {
      com
        .send('request_floor')
        .then(() => this.notify('You have been added to the queue'))
        .catch(err => this.notify(err.message, 'is-danger'));
    },
    withdrawFromQueue() {
      com
        .send('withdraw_from_queue')
        .then(() => this.notify('You have been removed from queue'))
        .catch(err => this.notify(err.message, 'is-danger'));
    },
    removeFromQueue(id) {
      com
        .send('remove_from_queue', { id })
        .then(() => this.notify('User have been removed from queue'))
        .catch(err => this.notify(err.message, 'is-danger'));
    },
    giveVoice(to) {
      const { name } = this.$store.getters['meeting/users'][to];
      com
        .send('give_voice', { to })
        .then(() => this.notify(`Voice have been given to ${name}`))
        .catch(err => this.notify(err.message, 'is-danger'));
    },
    notify(message, type) {
      this.$bus.emit('notification', { message, type: type || 'is-success' });
    }
  }
};
</script>

<style scoped>
.speaker-name {
  font-size: 350%;
}
</style>
