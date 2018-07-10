<template>
  <div>
    <div class="columns">
      <div class="column is-8 is-offset-2">
        <p class="title">
          Welcome back, {{ name }}!
        </p>
        <Schedule/>
      </div>
    </div>
  </div>
</template>

<script>
import Schedule from '@/components/Schedule.vue';

export default {
  layout: 'portal',
  components: { Schedule },
  computed: {
    name() {
      return this.$auth.user.name;
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/meetings/fetchPage', { max_results: 50 });
    await store.dispatch('names/fetch', { collection: 'proposals', field: 'title' });
  }
};
</script>
