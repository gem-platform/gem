<template>
  <div>
    <div
      v-if="speaker"
      class="speaker-block">
      <div class="speaker-name">{{ speaker.name }}</div>
      is speaking now
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiscussionStageView',
  computed: {
    speaker() {
      const { speaker } = this.$store.getters.meetingStageState;
      const { users } = this.$store.getters;
      return users[speaker];
    },
  },
};
</script>

<style scoped>
.speaker-name {
  font-size: 350%
}
</style>
