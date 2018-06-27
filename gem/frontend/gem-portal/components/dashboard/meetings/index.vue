<template>
  <div>
    <b-table
      :data="entities"
      :columns="columns"
      hoverable>
      <template slot-scope="props">
        <b-table-column
          field="id"
          label="Title">
          <nuxt-link :to="viewUrl(props.row._id)">{{ props.row.title || 'No title' }}</nuxt-link>
        </b-table-column>
        <b-table-column
          field="id"
          label="Actions"
          class="has-text-centered">
          <nuxt-link
            v-if="props.row.proposals"
            :to="/meeting/+props.row._id"
            class="button is-primary is-small">
            <span class="icon is-small">
              <i class="fa fa-play"/>
            </span>
            <span>Start</span>
          </nuxt-link>
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
        },
        {
          field: 'id',
          label: 'Actions'
        }
      ];
    }
  }
};
</script>
