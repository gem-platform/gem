<template>
  <div>
    <div
      v-for="(role, name) in users"
      :key="name"
      class="notification">
      <span class="heading has-text-centered">
        {{ name }}
        ({{ role.length }})
      </span>
      <ul>
        <li
          v-for="user in role"
          :key="user.name">
          <span class="icon">
            <i class="fa fa-user"/>
          </span>
          <span>{{ user.name }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  data() {
    return {
      users: []
    };
  },
  computed: {
    allUsers() {
      return this.$store.getters['meeting/users'];
    },
    allRoles() {
      return this.$store.getters['meeting/roles'];
    }
  },
  mounted() {
    this.$socket.on('meeting_users_online', this.onData);
  },
  beforeDestroy() {
    this.$socket.off('meeting_users_online', this.onData);
  },
  methods: {
    onData(data) {
      this.users = data
        .map(uid => this.allUsers[uid])
        .map(user => ({
          name: user.name,
          role: this.allRoles[user.roles[0]].name
        }));

      this.users = _.groupBy(this.users, u => u.role);
    }
  }
};
</script>

<style>

</style>
