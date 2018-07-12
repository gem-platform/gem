<template>
  <div>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link
          :to="linkToCreate()"
          class="button is-light">
          <span class="icon">
            <i class="fa fa-plus"/>
          </span>
          <span>Create new</span>
        </nuxt-link>
      </p>
    </div>

    <b-table
      :data="entities"
      :columns="columns"
      :current-page.sync="currentPage"
      :per-page="perPage"
      :total="total"
      :loading="loading"
      hoverable
      paginated
      backend-pagination
      @page-change="onPageChange">
      <template slot-scope="props">
        <b-table-column
          v-for="(column, idx) in columns"
          :key="column.title">

          <nuxt-link
            v-if="idx === 0"
            :to="linkToEdit(props.row._id)">
            {{ columnText(props.row, column) }}
          </nuxt-link>
          <span v-else>
            {{ columnText(props.row, column) }}
          </span>

        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import CrudLinksComponentMixin from '@/components/CrudLinksComponentMixin';
import CrudIndexComponents from '@/lib/crud/components/index';

export default {
  layout: 'dashboard',
  mixins: [CrudLinksComponentMixin],
  data() {
    return {
      loading: false,
      currentPage: 1,
      perPage: 25
    };
  },
  computed: {
    /**
     * Return list of entities to display at index page
     */
    entities() {
      const store = this.$store.getters[`dashboard/${this.component}/paginated`];
      if (!store) { throw Error(`No "paginated" getter for "${this.component}" entity`); }
      return store[this.currentPage];
    },

    /**
     * Get type of component to render at page
     */
    component() {
      return this.$route.params.entities;
    },

    /**
     * Total records
     */
    total() {
      return this.$store.getters[`dashboard/${this.component}/meta`].total;
    },

    /**
     * Columns for table
     */
    columns() {
      const config = CrudIndexComponents[this.component];
      return config.columns;
    }

  },

  methods: {
    /**
     * Page changed
     */
    async onPageChange(page) {
      this.loading = true;
      await this.$store.dispatch(`dashboard/${this.component}/fetchPage`, { page });
      this.loading = false;
    },

    /**
     * Get text for cell
     */
    columnText(row, column) {
      return typeof column.field === 'function'
        ? column.field(row, this)
        : row[column.field];
    }
  },

  /**
   * Fetch data for page
   */
  async fetch(context) {
    const options = CrudIndexComponents[context.params.entities];
    const method = `dashboard/${context.params.entities}/fetchPage`;
    await context.store.dispatch(method);

    if (options && options.fetch) {
      await options.fetch(context);
    }
  }
};
</script>
