<template>
  <div>
    <b-table
      :data="entities"
      :columns="columns">
      <template slot-scope="props">
        <b-table-column
          field="id"
          label="Title">
          <nuxt-link :to="viewUrl(props.row._id)">{{ props.row.title || 'No title' }}</nuxt-link>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  props: {
    entities: {
      type: Array,
      required: true
    },
    viewUrl: {
      type: Function,
      default: () => {}
    }
  },
  computed: {
    columns() {
      return [
        {
          field: 'title',
          label: 'Title'
        }
      ];
    }
  }
};
</script>
