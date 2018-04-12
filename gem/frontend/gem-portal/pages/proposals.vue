<template>
  <div>
    <b-table
      :data="proposals"
      :columns="columns">
    </b-table>
    {{proposals}}
  </div>
</template>

<script>
export default {
  computed: {
    proposals() {
      return this.$store.getters['dashboard/proposals/all'];
    },
    columns() {
      return [
        {
          field: 'title',
          label: 'Title'
        }
      ];
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/proposals/fetch');
    /*const res = await $axios.get('http://localhost:5000/proposal');
    this.items = res.data._items;
    console.log(res.data._items);*/
  }
};
</script>

<style>

</style>
