<template>
  <div>
    <!-- Reading progress bar -->
    <progress
      :value="progress"
      class="progress is-primary is-large"
      max="100"/>

    <!-- List of users still reading the proposal -->
    <div v-if="notReadYet.length > 0">
      Still reading:
      <div
        v-for="user in notReadYet"
        :key="user.name">
        {{ user.name }}: {{ user.progress }}%
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AcquaintanceStageView',
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
      const { progress } = this.$store.getters['meeting/stage/state'];
      const percentages = Object.values(progress);

      if (percentages.length > 0) {
        const sum = percentages.reduce((a, b) => a + b, 0);
        return (sum / percentages.length) * 100;
      }

      return 0;
    },

    /**
     * Returns a list of users who have not finished reading
     */
    notReadYet() {
      const { progress } = this.$store.getters['meeting/stage/state'];

      return Object.entries(progress)
        .map(x => ({
          name: this.users[x[0]].name,
          progress: Math.floor(x[1] * 100)
        }))
        .filter(x => x.progress < 100);
    }
  }
};
</script>
