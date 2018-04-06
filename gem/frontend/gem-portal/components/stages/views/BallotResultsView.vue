<template>
  <div>
    <b-table
      :data="summaryData"
      :columns="summaryColumns"/>
  </div>
</template>

<script>
export default {
  name: "BallotResultsStageView",
  computed: {
    votes() {
      const votes = this.$store.getters["meeting/meetingStageState"];
      const users = this.$store.getters["meeting/users"];
      const roles = this.$store.getters["meeting/roles"];

      const result = votes.map(x => ({
        name: users[x.user_id].name,
        roles: users[x.user_id].roles.map(r => roles[r].name).join(", "),
        value: x.value
      }));

      return result;
    },
    summaryData() {
      const summary = this.$store.getters["meeting/meetingStageState"].summary;
      const roles = this.$store.getters["meeting/roles"];

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
        { field: "role", label: "Role" },
        { field: "yes", label: "Yes" },
        { field: "no", label: "No" },
        { field: "abstained", label: "Abstained" }
      ];
    }
  }
};
</script>
