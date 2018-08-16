<template>
  <div>
    <b-field grouped>
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
      <b-input
        v-if="searchColumn"
        v-model.trim="searchQuery"
        expanded
        type="search"
        icon="fas fa-search"
        placeholder="Search"
        @input="searchQueryChanged"/>
    </b-field>

    <b-table
      :data="entities"
      :current-page.sync="currentPage"
      :per-page="perPage"
      :total="total"
      :loading="loading"
      :default-sort="defaultSort"
      default-sort-direction="asc"
      hoverable
      paginated
      backend-pagination
      backend-sorting
      @page-change="pageChanged"
      @sort="onSort">
      <template slot-scope="props">
        <b-table-column
          v-for="(column, idx) in columns"
          :key="column.label"
          :label="column.label"
          :field="column.sortable ? column.field : undefined"
          :sortable="column.sortable">

          <nuxt-link
            v-if="idx === 0"
            :to="indexLinkToEdit ? linkToEdit(props.row._id) : linkToView(props.row._id)">
            {{ columnText(props.row, column) }}
          </nuxt-link>
          <span v-else>
            {{ columnText(props.row, column) }}
          </span>

        </b-table-column>
      </template>

      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>
              <b-icon
                icon="fas fa-frown-o"
                size="is-large"/>
            </p>
            <p>Nothing found.</p>
          </div>
        </section>
      </template>
    </b-table>
  </div>
</template>

<script>
import CrudLinksComponentMixin from '@/components/CrudLinksComponentMixin';
import CrudIndexComponents from '@/lib/crud/components/index';
import _ from 'lodash';

export default {
  layout: 'dashboard',
  mixins: [CrudLinksComponentMixin],
  data() {
    const component = this.$route.params.entities;
    const config = CrudIndexComponents[component];

    return {
      loading: false,
      currentPage: 1,
      perPage: 25,
      searchQuery: '',
      sortColumn: undefined,
      sortOrder: undefined,
      defaultSort: config.defaultSort
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
    },

    /**
     * Search column
     */
    searchColumn() {
      const config = CrudIndexComponents[this.component];
      return config.searchColumn;
    },

    /**
     * Columns for table
     */
    indexLinkToEdit() {
      const config = CrudIndexComponents[this.component];
      return config.indexLinkToEdit;
    }
  },

  methods: {
    onSort(column, order) {
      this.sortColumn = column;
      this.sortOrder = order;
      this.loadData();
    },

    /**
     * Load data
     */
    async loadData() {
      this.loading = true;

      // query
      const query = {
        page: this.currentPage
      };

      // if search column and query provided
      if (this.searchColumn && this.searchQuery) {
        const regex = _.escapeRegExp(this.searchQuery);
        query.where = {
          [this.searchColumn]: { $regex: `(?i).*${regex}.*` }
        };
      }

      // if sort column provided
      if (this.sortColumn) {
        query.sort = this.sortOrder === 'asc' ? this.sortColumn : `-${this.sortColumn}`;
      }

      // fetch
      await this.$store.dispatch(`dashboard/${this.component}/fetchPage`, query);
      this.loading = false;
    },

    /**
     * Page changed
     */
    async pageChanged(page) {
      this.currentPage = page;
      this.loadData();
    },

    /**
     * Search query changed
     */
    searchQueryChanged: _.debounce(function loadDataDebounced() {
      this.loadData();
    }, 350),

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
    const result = await context.store.dispatch(method);

    if (options && options.fetch) {
      await options.fetch(context, result);
    }
  }
};
</script>
