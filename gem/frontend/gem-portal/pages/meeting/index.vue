<template>
  <div>
    <div
      v-for="meeting in meetings"
      :key="meeting._id">
      <nuxt-link :to="'/meeting/'+meeting._id">{{ meeting.title }}</nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'portal',
  computed: {
    meetings() {
      return this.$store.getters['dashboard/meetings/all'];
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/meetings/fetch');
  }
};
</script>

<style>

</style>
