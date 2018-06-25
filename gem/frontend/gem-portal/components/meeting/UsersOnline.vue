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

      <div
        v-for="user in role"
        :key="user.name"
        class="level">
        <div class="level-left">
          <div class="level-item">
            <span class="icon">
              <i class="fa fa-user"/>
            </span>
            <span>
              {{ user.name }}
            </span>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
            <i
              v-if="userInactive(user.id)"
              class="fa fa-bed has-text-grey-light"/>
          </div>
        </div>
      </div>
    </div>
</div></template>

<script>
import _ from 'lodash';

export default {
  data() {
    return {
      users: [],
      afk: []
    };
  },
  computed: {
    /**
     * Returns list of useers able to be at meeting
     */
    allUsers() {
      return this.$store.getters['meeting/users'];
    },

    /**
     * Return all roles able to be at meeting
     */
    allRoles() {
      return this.$store.getters['meeting/roles'];
    }
  },
  mounted() {
    this.$socket.on('meeting_users_online', this.onOnlineUsersData);
    this.$socket.on('inactive_users', this.onInactiveUsersData);

    this.$socket.emit('meeting_users_online', {}, res => this.onOnlineUsersData(res.online));
  },
  beforeDestroy() {
    this.$socket.off('meeting_users_online', this.onOnlineUsersData);
    this.$socket.off('inactive_users', this.onInactiveUsersData);
  },
  methods: {
    /**
     * Is the user inactive or not?
     */
    userInactive(id) {
      return this.afk.includes(id);
    },

    /**
     * List of online users have arrived
     */
    onOnlineUsersData(data) {
      this.users = data
        .map(uid => this.allUsers[uid])
        .map(user => ({
          id: user.id,
          name: user.name,
          role: this.allRoles[user.roles[0]].name
        }));

      this.users = _.groupBy(this.users, u => u.role);
    },

    /**
     * List of inactive users have arrived
     */
    onInactiveUsersData(data) {
      this.afk = data;
    }
  }
};
</script>

<style scoped>
.level {
  margin-bottom: 0em;
}
</style>
