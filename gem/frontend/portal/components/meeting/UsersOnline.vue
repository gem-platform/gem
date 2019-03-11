<template>
  <div>

    <!-- List of requests to access -->
    <div
      v-if="canManage && requests.length > 0"
      class="notification is-danger">

      <!-- Header -->
      <span class="heading has-text-centered">
        Access Requests
      </span>

      <!-- List of users -->
      <div
        v-for="user in requests"
        :key="user.id">

        <span class="icon">
          <i class="fa fa-user"/>
        </span>
        <span>
          {{ user.name }} ({{ user.role }})
        </span>

        <b-tooltip label="Grant access rights">
          <span
            class="icon"
            @click="grantAccessRights(user, true)">
            <i class="fa fa-check"/>
          </span>
        </b-tooltip>

        <b-tooltip label="Reject request">
          <span
            class="icon"
            @click="grantAccessRights(user, false)">
            <i class="fa fa-times"/>
          </span>
        </b-tooltip>

      </div>
    </div>

    <!-- Online users grouped by role -->
    <div
      v-for="(role, name) in users"
      :key="name"
      class="notification">
      <span class="heading has-text-centered">
        {{ name }}
        ({{ role.length }})
      </span>

      <div
        v-for="user in role"
        :key="user.name">
        <span class="icon">
          <i
            v-if="user.meta && user.meta.inactive"
            class="fa fa-bed has-text-grey-light"/>
          <i
            v-else
            class="fa fa-user"/>
        </span>
        <span>
          {{ user.name }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';

import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';

export default {
  mixins: [AuthMixin, NotificationMixin],
  computed: {
    canManage() {
      return this.haveAccess('meeting.manage');
    },
    users() {
      const { usersOnline } = this.$store.state.meeting;
      return _.groupBy(usersOnline.online, u => u.role);
    },
    requests() {
      const { usersOnline } = this.$store.state.meeting;
      return usersOnline.requests || [];
    }
  },
  methods: {
    /**
     * Grant access rights to specified user
     */
    grantAccessRights(user, value) {
      this.notify(value
        ? `Access granted to ${user.name}`
        : `Access request from ${user.name} rejected`);

      this.$socket.emit('grant_access', { token: user.id, value });
    }
  }
};
</script>

<style scoped>
.level {
  margin-bottom: 0em;
}
</style>
