<template>
  <div>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link :to="newUrl" class="button is-light">Create new</nuxt-link>
      </p>
    </div>

    <b-table
      :data="entities"
      :columns="columns">
      <template slot-scope="props">
        <b-table-column field="id" label="Index">
          <nuxt-link :to="viewUrl(props.row._id)">{{ props.row.index || 'Undefined' }}</nuxt-link>
        </b-table-column>

        <b-table-column field="title" label="Title">
          {{ props.row.title }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';

export default {
  layout: 'portal',
  mixins: [CrudComponentMixin()],
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
