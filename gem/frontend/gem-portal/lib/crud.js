export default class CrudController {
  constructor(options) {
    this.idField = options.idField || 'id';
    this.apiPrefix = options.apiPrefix;
    this.storePrefix = options.storePrefix;
    this.fields = options.fields;
  }

  entity({ id, store }) {
    // Nothing to fetch, return dummy object filled
    // with keys from this.fields
    if (id == '@new') return _.zipObject(this.fields);

    // Find entity using specified getter
    const getterName = this.storePrefix + 'all';
    const getter = store.getters[getterName];
    const entity = getter.find(i => i[this.idField] == id);

    // Return only fields provided in this.fields
    return _.pick({ ...entity }, this.fields);
  }

  async submit({ id, data, store, axios }) {
    const method = id ? 'update' : 'create';
    await store.dispatch(this.storePrefix + method, data);
  }

  async fetch({ id, store }) {
    // Nothing to fetch, it is a new object
    if (id == '@new') return;

    // Fetch data using store action
    const method = this.storePrefix + 'fetch';
    await store.dispatch(method, { [this.idField]: id });
  }
}
