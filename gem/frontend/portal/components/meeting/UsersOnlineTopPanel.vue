<template>
  <div>
    <nav class="level is-mobile box notification">
      <div
        class="level-item has-text-centered">
        <div>
          <p class="heading">Total</p>
          <p class="title">{{ usersCount }}</p>
        </div>
      </div>

      <div
        v-for="(value, user) in users"
        :key="value"
        class="level-item has-text-centered">
        <div>
          <p class="heading">{{ user }}</p>
          <p class="title">{{ value }}</p>
        </div>
      </div>

      <div
        class="level-item has-text-centered">
        <div>
          <p
            :class="quorumStyle"
            class="heading">
            Quorum
          </p>
          <p
            :class="quorumStyle"
            class="title">
            {{ isQuorumMet | quorum }}
          </p>
        </div>
      </div>

    </nav>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  filters: {
    quorum(value) {
      return value ? 'Met' : 'Not Met';
    }
  },
  computed: {
    isQuorumMet() {
      // todo: rewrite using meeting configuration
      return this.usersCount >= 19;
    },
    quorumStyle() {
      return this.isQuorumMet ? 'has-text-success' : 'has-text-danger';
    },
    users() {
      const { usersOnline } = this.$store.state.meeting;
      const groupedByRole = _.groupBy(usersOnline.online, u => u.role);
      const result = _.mapValues(groupedByRole, o => o.length);

      return result;
    },
    usersCount() {
      const result = this.users;
      return Object.values(result).reduce((a, b) => a + b, 0);
    }
  }
};
</script>

