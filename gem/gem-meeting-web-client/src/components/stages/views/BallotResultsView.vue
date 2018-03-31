<template>
  <div>
    <b-table
      :data="votes"
      :columns="columns"/>
  </div>
</template>

<script>
export default {
  name: 'BallotResultsStageView',
  computed: {
    votes() {
      const { votes } = this.$store.getters.meetingStageState;
      const { users } = this.$store.getters;
      const voteKeys = Object.keys(votes);
      const result = voteKeys.map(x => ({
        name: users[x].name,
        value: votes[x],
        all: users[x]
      }));
      return result;
    },
    columns() {
      return [
        { field: 'name', label: 'Name' },
        { field: 'value', label: 'Value', width: '100' }
      ];
    }
  }
};
</script>
