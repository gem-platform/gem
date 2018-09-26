<template>
  <div>
    <GlobalMessage
      :title="title"
      :message="message"
      :class="type"/>

    <div class="box">
      <!-- Actions response help message -->
      <b-message
        v-if="actionHelpMessage"
        :type="actionHelpClass">
        {{ actionHelpMessage }}
      </b-message>

      <!-- Actions to do -->
      <div
        v-if="actions.length > 0">
        <b-field
          v-for="action in actions"
          :key="action">
          <button
            class="button is-fullwidth"
            @click="runAction(action)">
            {{ action | human }}
          </button>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';

import GlobalMessage from '@/components/GlobalMessage.vue';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'ConnectingScreen',
  filters: {
    /**
     * Returns a human readable version of specified command
     */
    human(value) {
      const clean = value.replace(/(-|_)/g, ' ');
      return _.capitalize(clean);
    }
  },
  components: {
    GlobalMessage
  },
  mixins: [CommunicationMixin],
  data() {
    return {
      actionHelpMessage: '', // help message,
      actionHelpClass: ''
    };
  },
  computed: {
    /**
     * Returns connection state
     */
    connection() {
      return this.$store.state.meeting.connection;
    },

    /**
     * Title for connection screen
     */
    title() {
      return this.connection.state;
    },

    /**
     * List of actions to do.
     */
    actions() {
      return this.connection.actions || [];
    },

    /**
     * Message for connection screen
     */
    message() {
      return this.connection.message || 'We are connecting you to session';
    },

    /**
     * Type of message
     */
    type() {
      return this.connection.state === 'disconnected' ? 'is-danger' : 'is-white';
    }
  },
  mounted() {
    this.$socket.on('open_meeting', (res) => {
      // this.$router.push({ path: `/meeting/${res}#reload` });
      window.location = `/meeting/${res}`; // todo: do it more VUE-way
    });
  },
  beforeDestroy() {
    this.$socket.off('open_meeting');
  },
  methods: {
    /**
     * Sends command to run specified action on server
     */
    async runAction(action) {
      const { token } = this.$auth.user;
      try {
        const res = await this.send(action, { token });
        this.actionHelpClass = 'is-success';
        this.actionHelpMessage = res.message;
      } catch (err) {
        this.actionHelpClass = 'is-danger';
        this.actionHelpMessage = err.message;
      }
    }
  }
};
</script>
