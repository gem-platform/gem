<template>
  <div>
    <b-table
      :data="proposals"
      :columns="columns">
      <template slot-scope="props">
        <b-table-column field="id" label="Index">
          <nuxt-link :to="proposalUrl(props.row.index)">{{ props.row.index }}</nuxt-link>
        </b-table-column>

        <b-table-column field="title" label="Title">
          {{ props.row.title }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  layout: 'portal',
  computed: {
    proposals() {
      return this.$store.getters['dashboard/proposals/all'];
    },
    columns() {
      return [
        {
          field: 'index',
          label: 'Index'
        },
        {
          field: 'title',
          label: 'Title'
        }
      ];
    }
  },
  methods: {
    proposalUrl(idx) {
      return '/dashboard/proposals/' + idx;
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/proposals/fetch');
  }
};
</script>
