<template>
  <div>
    <!-- Reading progress bar -->
    <p class="heading has-text-centered">
      Reading progress
    </p>
    <progress
      :value="progress"
      class="progress is-primary is-large"
      max="100"/>

    <!-- List of users still reading the proposal -->
    <b-table
      v-if="showReaders"
      :data="readers">

      <template slot-scope="props">
        <b-table-column
          label="Name"
          sortable
          field="name">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          label="Progress"
          sortable
          numeric
          field="progress">
          {{ props.row.progress }}%
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import AuthMixin from '@/components/AuthMixin';

export default {
  name: 'AcquaintanceStageView',
  mixins: [StageStateMixin, AuthMixin],
  computed: {
    /**
     * Get list of users present on the meeting.
     */
    users() {
      return this.$store.getters['meeting/users'];
    },

    /**
     * Returns the average percentage of reading the proposal
     */
    progress() {
      const { count, values } = this.$stage.readingProgress;
      const percentages = Object.values(values);

      if (count > 0) {
        const sum = percentages.reduce((a, b) => a + b, 0);
        return (sum / count) * 100;
      }

      return 0;
    },

    /**
     * Returns a list of users who have not finished reading
     */
    readers() {
      const users = Object.entries(this.users);
      const progress = this.$stage.readingProgress.values;

      return users
        .map(x => ({
          name: x[1].name,
          progress: Math.floor((progress[x[0]] || 0) * 100)
        }))
        .filter(x => x.progress < 100)
        .sort((a, b) => (a.progress < b.progress ? 1 : -1));
    },

    /**
     * Show readers block or not?
     */
    showReaders() {
      const { config } = this.$stage;

      return (
        this.readers.length > 0 && // there are some users still reading
        this.haveAccess('meeting.manage') &&
        config && config.proposalDisplayMode === 'in-parts'); // it is a secretary
    },

    /**
     * Show reading progress?
     */
    showReadingProgress() {
      const { config } = this.$stage;
      return config && config.proposalDisplayMode === 'in-parts';
    }
  }
};
</script>
