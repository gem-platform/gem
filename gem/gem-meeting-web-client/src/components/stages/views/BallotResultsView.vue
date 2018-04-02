<template>
  <div>

    <b-table
      :data="summary"
      :columns="summaryColumns"/>
    <b-table
      :data="votes"
      :columns="detailColumns"/>
  </div>
</template>

<script>
export default {
  name: 'BallotResultsStageView',
  computed: {
    votes() {
      const { votes } = this.$store.getters.meetingStageState;
      const { users, roles } = this.$store.getters;

      const result = votes.map(x => ({
        name: users[x.user_id].name,
        roles: users[x.user_id].roles.map(r => roles[r].name).join(', '),
        value: x.value
      }));

      return result;
    },
    summary() {
      const { summary } = this.$store.getters.meetingStageState;
      const { roles } = this.$store.getters;

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
    },
    detailColumns() {
      return [
        { field: 'name', label: 'Name' },
        { field: 'roles', label: 'Roles' },
        { field: 'value', label: 'Value', width: '100' }
      ];
    }
  }
};
</script>
