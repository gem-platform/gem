<template>
  <div>
    <!-- Reading progress bar -->
    <progress
      :value="progress"
      class="progress is-primary is-large"
      max="100"/>

    <!-- List of users still reading the proposal -->
    <div v-if="showReaders">
      Still reading:
      <div
        v-for="user in readers"
        :key="user.name">
        {{ user.name }}: {{ user.progress }}%
      </div>
    </div>

    <CommentsList/>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import AuthMixin from '@/components/AuthMixin';
import CommentsList from '@/components/meeting/stages/widgets/CommentsList.vue';

export default {
  name: 'AcquaintanceStageView',
  components: { CommentsList },
  mixins: [StageStateMixin, AuthMixin],
  data() {
    return {
      users: this.$store.getters['meeting/users']
    };
  },
  computed: {
    /**
     * Returns the average percentage of reading the proposal
     */
    progress() {
      const { count, values } = this.$stage.progress;
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
      return Object.entries(this.$stage.progress.values)
        .map(x => ({
          name: this.users[x[0]].name,
          progress: Math.floor(x[1] * 100)
        }))
        .filter(x => x.progress < 100);
    },

    /**
     * Show readers block or not?
     */
    showReaders() {
      return (
        this.readers.length > 0 && // there are some users still reading
        this.haveAccess('meeting.manage')); // it is a secretary
    }
  }
};
</script>
