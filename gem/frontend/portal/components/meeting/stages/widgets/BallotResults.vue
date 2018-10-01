<template>
  <div>
    <p
      v-if="header"
      class="heading has-text-centered">
      {{ header }}
    </p>

    <b-table
      v-if="summaryData.length > 0"
      :data="summaryData"
      :columns="summaryColumns"/>
    <div
      v-else
      class="has-text-centered">
      There is no ballot results.
    </div>
  </div>
</template>

<script>
export default {
  name: 'BallotResults',
  props: {
    header: {
      type: String,
      default() { return 'Ballot results'; }
    }
  },
  computed: {
    votes() {
      const votes = this.$store.getters['meeting/stage/state'];
      const users = this.$store.getters['meeting/users'];
      const roles = this.$store.getters['meeting/roles'];

      const result = votes.map(x => ({
        name: users[x.user_id].name,
        roles: users[x.user_id].roles.map(r => roles[r].name).join(', '),
        value: x.value
      }));

      return result;
    },
    summaryData() {
      const state = this.$store.getters['meeting/stage/state'];
      const summary = state.summary || state.ballotSummary;
      const roles = this.$store.getters['meeting/roles'];

      const roleIds = Object.keys(summary);
      const result = roleIds.map(x => ({
        role: roles[x].name,
        yes: summary[x].yes,
        no: summary[x].no,
        abstained: summary[x].abstained
      }));

      return result;
    },
    summaryColumns() {
      return [
        { field: 'role', label: 'Role' },
        { field: 'yes', label: 'Yes' },
        { field: 'no', label: 'No' },
        { field: 'abstained', label: 'Abstained' }
      ];
    }
  }
};
</script>
