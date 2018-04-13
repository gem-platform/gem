<template>
  <div class="content">
    <h1>{{id}}:{{ title }}</h1>
    {{ content }}
  </div>
</template>

<script>
export default {
  layout: 'portal',
  computed: {
    id() {
      return this.proposal.index;
    },
    title() {
      return this.proposal.title;
    },
    content() {
      return this.proposal.content;
    },
    proposal() {
      const proposalIndex = this.$route.params.id;
      return this.$store.getters['dashboard/proposals/get'](proposalIndex)[0];
    }
  },
  async fetch({ store, route }) {
    const id = route.params.id;
    await store.dispatch('dashboard/proposals/fetch', { index: id });
  }
};
</script>
