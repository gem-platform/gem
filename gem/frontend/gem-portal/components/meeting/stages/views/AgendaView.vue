<template>
  <div>
    {{ content }}
  </div>
</template>

<script>
export default {
  name: 'AgendaStageView',
  computed: {
    content() {
      const { meetingStageState } = this.$store.getters;
      return meetingStageState
        ? meetingStageState.content
        : 'No content provided';
    }
  }
};
</script>
