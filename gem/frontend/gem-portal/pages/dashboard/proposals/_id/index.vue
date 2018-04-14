<template>
  <div class="content">
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link :to="editUrl" class="button is-light">Edit</nuxt-link>
      </p>
      <p class="control">
        <nuxt-link :to="deleteUrl" class="button is-light">Delete</nuxt-link>
      </p>
    </div>
    
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
    },
    editUrl() {
      const proposalIndex = this.$route.params.id;
      return '/dashboard/proposals/' + proposalIndex + '/edit';
    },
    deleteUrl() {
      const proposalIndex = this.$route.params.id;
      return '/dashboard/proposals/' + proposalIndex + '/delete';
    }
  },
  async fetch({ store, route }) {
    const id = route.params.id;
    await store.dispatch('dashboard/proposals/fetch', { index: id });
  }
};
</script>
