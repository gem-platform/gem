<template>
  <div>
    <div v-if="canDiscuss">
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
                @click="giveVoice(props.row.id)">
                <span class="icon">
                  <i class="fa fa-microphone"/>
                </span>
              </a>
            </b-tooltip>

            <!-- Remove from queue -->
            <b-tooltip
              label="Remove from queue"
              position="is-left">
              <a
                class="button is-white is-small"
                @click="removeFromQueue(props.row.id)">
                <span class="icon">
                  <i class="fa fa-trash"/>
                </span>
              </a>
            </b-tooltip>
          </b-table-column>
        </template>
      </b-table>
    </div>

    <!-- Have no rights -->
    <div
      v-else
      class="has-text-danger has-text-centered">
      You have no rights to discuss.
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'DiscussionStageControls',
  mixins: [AuthMixin, NotificationMixin, StageStateMixin, CommunicationMixin],
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
      return this.$stage.queue.includes(this.user.id);
    },

    /**
     * Can user manage current stage or not?
     */
    canManage() {
      return this.haveAccess('meeting.manage');
    },

    /**
     * Can user discuss or not
     */
    canDiscuss() {
      return this.haveAccess('meeting.discuss');
    }
  },
  methods: {
    /**
     * Request a floor
     */
    async requestFloor() {
      try {
        await this.send('request_floor');
        this.notify('You have been added to the queue');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Withraw from queue
     */
    async withdrawFromQueue() {
      try {
        await this.send('withdraw_from_queue');
        this.notify('You have been removed from queue');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Remove user from queue using specified user's ID
     */
    async removeFromQueue(id) {
      try {
        await this.send('remove_from_queue', { id });
        this.notify('User have been removed from queue');
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    },

    /**
     * Give a voice to specified user
     */
    async giveVoice(to) {
      const { name } = this.$store.getters['meeting/users'][to];
      try {
        await this.send('give_voice', { to });
        this.notify(`Voice have been given to ${name}`);
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    }
  }
};
</script>

<style scoped>
.speaker-name {
  font-size: 5em;
}
</style>
