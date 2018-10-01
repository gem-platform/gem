<template>
  <div>
    <b-message
      v-if="secret">
      This is a secret ballot. You can not see the details.
    </b-message>

    <b-table
      :data="summaryData"
      :columns="summaryColumns"
      :detailed="!secret"
      detail-key="role">
      <template
        slot="detail"
        slot-scope="props">

        <div
          v-for="(users, vote) in props.row.users"
          :key="vote">

          <p class="heading has-text-centered">{{ vote }}</p>
          <div
            v-for="user in users"
            :key="user.id">{{ user.name }}</div>
        </div>

      </template>
    </b-table>

  </div>
</template>

<script>
import _ from 'lodash';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'BallotResults',
  mixins: [StageStateMixin],
  computed: {
    summaryData() {
      const state = this.$store.getters['meeting/stage/state'];
      const summary = (state.summary || state.ballotSummary).votes;
      const roles = this.$store.getters['meeting/roles'];
      const users = this.$store.getters['meeting/users'];

      const roleIds = Object.keys(summary);
      const result = roleIds.map(x => ({
        role: roles[x].name,
        yes: summary[x].yes,
        no: summary[x].no,
        abstained: summary[x].abstained,
        users: _.groupBy(summary[x].users.map(u => ({
          id: u.id,
          name: users[u.id].name,
          value: u.value
        })), 'value')
      }));

      return result;
    },
    secret() {
      return (this.$stage.summary || this.$stage.ballotSummary).secret;
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
