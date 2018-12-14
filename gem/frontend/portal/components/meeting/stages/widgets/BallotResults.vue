<template>
  <div>
    <p
      v-if="header"
      class="heading has-text-centered">
      {{ header }}
    </p>

    <div
      v-if="summaryData.length > 0">

      <div
        v-if="showResult"
        :class="{'is-success': result=='pass',
                 'is-danger': result=='fail',
                 'is-warning': result=='tie'}"
        class="notification has-text-centered is-size-4">
        {{ result | ballotResult }}
      </div>

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

    <div
      v-else
      class="has-text-centered">
      There is no ballot results.
    </div>

  </div>
</template>

<script>
import _ from 'lodash';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'BallotResults',
  filters: {
    ballotResult(value) {
      if (value === 'pass') { return 'Pass'; }
      if (value === 'fail') { return 'Fail'; }
      if (value === 'tie') { return 'Tie'; }
      return value;
    }
  },
  mixins: [StageStateMixin],
  props: {
    header: {
      type: String,
      default() { return 'Ballot results'; }
    },
    showResult: {
      type: Boolean,
      default() { return false; }
    }
  },
  computed: {
    summaryData() {
      const state = this.$store.getters['meeting/stage/state'];
      const summary = (state.summary || state.ballotSummary).votes;
      const roles = this.$store.getters['meeting/roles'];
      const users = this.$store.getters['meeting/users'];

      if (!summary) {
        return {};
      }

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
    result() {
      return (this.$stage.summary || this.$stage.ballotSummary).result;
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
