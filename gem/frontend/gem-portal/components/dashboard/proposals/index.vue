<template>
  <div>
    <b-table
      :data="entities"
      :columns="columns"
      hoverable="true">
      <template slot-scope="props">
        <b-table-column
          field="id"
          label="Index">
          <nuxt-link :to="viewUrl(props.row._id)">{{ props.row.index || 'Undefined' }}</nuxt-link>
        </b-table-column>

        <b-table-column
          field="title"
          label="Title">
          {{ props.row.title }}
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
          field: 'index',
          label: 'Index'
        },
        {
          field: 'title',
          label: 'Title'
        }
      ];
    }
  }
};
</script>
