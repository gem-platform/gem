<template>
  <div>
    <!-- "Request a floor" / "Withdaw from queue" buttons -->
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

    <!-- Queue -->
    <b-table
      :data="queue"
      :columns="columns">

      <!-- If queue is empty -->
      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            Queue is empty.
          </div>
        </section>
      </template>

      <!-- Columns -->
      <template slot-scope="props">
        <!-- Name column -->
        <b-table-column label="Name">
          {{ props.row.name }}
        </b-table-column>

        <!-- Actions column -->
        <b-table-column
          v-if="canManage"
          label="Actions">

          <!-- Give a voice -->
          <b-tooltip
            label="Give a voice"
            position="is-left">
            <a
              class="button is-white is-small"
              @click="giveVoice(props.row.id)">V</a>
          </b-tooltip>

          <!-- Remove from queue -->
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
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'DiscussionStageControls',
  mixins: [AuthMixin, NotificationMixin, StageStateMixin],
  computed: {
    columns() {
      const columns = [{ field: 'name', label: 'Name' }];

      // append "Actions" column for user with apropriate rights
      if (this.canManage) {
        columns.push({ field: 'id', label: 'Actions', width: '100' });
      }
      return columns;
    },

    /**
     * Discussion queue
     */
    queue() {
      const users = this.$store.getters['meeting/users'];
      return this.$stage.queue.map(x => users[x]);
    },

    /**
     * Is the current user in the queue?
     */
    selfInQueue() {
      const user = this.$store.getters['meeting/user'];
      return this.$stage.queue.includes(user.id);
    },

    /**
     * Can user manage current stage or not?
     */
    canManage() {
      return this.haveAccess('meeting.manage');
    }
  },
  methods: {
    /**
     * Request a floor
     */
    async requestFloor() {
      const res = await com.send('request_floor');
      this.notify(
        res.success ? 'You have been added to the queue' : res.message,
        res.success ? 'is-success' : 'is-danger'
      );
    },

    /**
     * Withraw from queue
     */
    async withdrawFromQueue() {
      const res = await com.send('withdraw_from_queue');
      this.notify(
        res.success ? 'You have been removed from queue' : res.message,
        res.success ? 'is-success' : 'is-danger'
      );
    },

    /**
     * Remove user from queue using specified user's ID
     */
    async removeFromQueue(id) {
      const res = await com.send('remove_from_queue', { id });
      this.notify(
        res.success ? 'User have been removed from queue' : res.message,
        res.success ? 'is-success' : 'is-danger'
      );
    },

    /**
     * Give a voice to specified user
     */
    async giveVoice(to) {
      const { name } = this.$store.getters['meeting/users'][to];
      const res = await com.send('give_voice', { to });
      this.notify(
        res.success ? `Voice have been given to ${name}` : res.message,
        res.success ? 'is-success' : 'is-danger'
      );
    }
  }
};
</script>

<style scoped>
.speaker-name {
  font-size: 5em;
}
</style>
