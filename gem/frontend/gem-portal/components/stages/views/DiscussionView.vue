<template>
  <div>
    <div
      v-if="speaker"
      class="speaker-block">
      <div class="speaker-name">{{ speaker.name }}</div>
      is speaking now
    </div>
    <div v-else>
      No one is speaking now
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiscussionStageView',
  computed: {
    speaker() {
      const speaker = this.$store.getters['meeting/stage/state'].speaker;
      const users = this.$store.getters['meeting/users'];
      return users[speaker];
    }
  }
};
</script>

<style scoped>
.speaker-name {
  font-size: 350%;
}
</style>
