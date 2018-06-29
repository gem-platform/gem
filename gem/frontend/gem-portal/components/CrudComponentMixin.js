import zipObject from 'lodash/zipObject';
import pick from 'lodash/pick';

export default {
  data() {
    return {
      busy: false
    };
  },
  computed: {
    entities() {
      const { entities } = this.$route.params;
      return this.$store.getters[`dashboard/${entities}/all`];
    },
    entity() {
      const fields = this.options && this.options.fields;
      const { id } = this.$route.params;

      // Nothing to fetch, return dummy object filled
      // with keys from this.fields
      if (id === '@new') return zipObject(fields);

      // Find entity using specified getter
      const getterName = this._storeMethod('all');
      const getter = this.$store.getters[getterName];
      const entity = getter.find(i => i._id === id);

      if (!entity) {
        return undefined;
      }

      // Return only fields provided in this.fields
      const keys = fields || Object.keys(entity);
      const ent = { ...entity };

      return pick(ent, keys);
    },
    newUrl() {
      return this._url({ id: '@new', action: 'edit' });
    },
    deleteUrl() {
      return this._url({ id: this.$route.params.id, action: 'delete' });
    }
  },
  methods: {
    viewUrl(id) {
      return this._url({ id });
    },
    editUrl(id) {
      return this._url({ id, action: 'edit' });
    },
    _storeMethod(method) {
      const { entities } = this.$route.params;
      return `dashboard/${entities}/${method}`;
    },
    _url(data) {
      data = data || {};
      const { entities } = this.$route.params;
      return `/dashboard/${entities}${data.id ? `/${data.id}` : ''}${
        data.action ? `/${data.action}` : ''
      }`;
    },
    async save() {
      try {
        this.busy = true;
        const id = this.entity._id;
        const data = this.entity;

        const method = id ? 'update' : 'create';
        await this.$store.dispatch(this._storeMethod(method), data);

        this.$router.push(this._url());
        this.$snackbar.open({ message: 'Proposal has been updated' });
      } catch (e) {
        const { response } = e;
        if (response.status === 422) {
          this.$snackbar.open({ message: 'Validation error', type: 'is-danger' });
        } else {
          this.$snackbar.open({ message: 'Unknown error', type: 'is-danger' });
        }
      } finally {
        this.busy = false;
      }
    },

    cancel() {
      this.$router.go(-1);
    },

    async remove() {
      try {
        this.busy = true;
        const id = this.entity._id;
        await this.$store.dispatch(this._storeMethod('remove'), { id });

        this.$router.push(this._url());
        this.$snackbar.open({ message: 'Proposal has been deleted' });
      } finally {
        this.busy = false;
      }
    }
  },
  async fetch({ store, params }) {
    try {
      this.busy = true;

      // call fetch method for component
      if (this.components[params.entities] && this.components[params.entities].fetch) {
        await this.components[params.entities].fetch({ store, params });
      }

      if (params.id === '@new') return;

      const method = `dashboard/${params.entities}/fetch`;
      await store.dispatch(method, params.id ? { _id: params.id } : undefined);
    } finally {
      this.busy = false;
    }
  }
};
