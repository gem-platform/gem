import _ from 'lodash';

export default (options) => {
  options = options || {};
  options.storePrefix = `dashboard/${options.entities}`;

  return {
    computed: {
      entities() {
        const entities = this.$route.params.entities || options.entities;
        return this.$store.getters[`dashboard/${entities}/all`];
      },
      entity() {
        const id = this.$route.params.id;

        // Nothing to fetch, return dummy object filled
        // with keys from this.fields
        if (id == '@new') return _.zipObject(options.fields);

        // Find entity using specified getter
        const getterName = this._storeMethod('all');
        const getter = this.$store.getters[getterName];
        const entity = getter.find(i => i._id == id);

        if (!entity) {
          return undefined;
        }

        // Return only fields provided in this.fields
        const keys = options.fields || Object.keys(entity);
        const ent = { ...entity };
        return _.pick(ent, keys);
      },
      newUrl() {
        return this._url({ id: '@new', action: 'edit' });
      },
      editUrl() {
        return this._url({ id: this.$route.params.id, action: 'edit' });
      },
      deleteUrl() {
        return this._url({ id: this.$route.params.id, action: 'delete' });
      }
    },
    methods: {
      viewUrl(id) {
        return this._url({ id });
      },
      _storeMethod(method) {
        const entities = this.$route.params.entities || options.entities;
        return `dashboard/${entities}/${method}`;
      },
      _url(data) {
        data = data || {};
        const entities = this.$route.params.entities || options.entities;
        return `/dashboard/${entities}${data.id ? `/${data.id}` : ''}${
          data.action ? `/${data.action}` : ''
        }`;
      },
      async save() {
        const id = this.entity._id;
        const data = this.entity;

        const method = id ? 'update' : 'create';
        await this.$store.dispatch(this._storeMethod(method), data);

        this.$router.push(this._url());
        this.$snackbar.open({ message: 'Proposal has been updated' });
      },

      async remove() {
        const id = this.entity._id;
        await this.$store.dispatch(this._storeMethod('remove'), { id });

        this.$router.push(this._url());
        this.$snackbar.open({ message: 'Proposal has been deleted' });
      }
    },
    async fetch({ store, params }) {
      if (params.id == '@new') return;

      const method = `dashboard/${params.entities || options.entities}/fetch`;
      await store.dispatch(method, params.id ? { _id: params.id } : undefined);
    }
  };
};
