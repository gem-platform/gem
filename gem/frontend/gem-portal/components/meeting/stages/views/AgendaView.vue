<template>
  <div>
    {{ content }}
  </div>
</template>

<script>
export default {
  name: 'AgendaStageView',
  computed: {
    /**
     * Returns agenda for current meeting
     */
    content() {
      const { content } = this.$store.getters['meeting/stage/state'];
      return content || 'No agenda provided';
    }
  }
};
</script>
