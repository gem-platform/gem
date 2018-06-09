<template>
  <div>
    <b-table
      :data="entities"
      :columns="columns"
      hoverable>
      <template slot-scope="props">
        <b-table-column
          field="id"
          label="Name">
          <nuxt-link :to="viewUrl(props.row._id)">{{ props.row.name || 'Noname' }}</nuxt-link>
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
          field: 'name',
          label: 'Name'
        }
      ];
    }
  }
};
</script>
