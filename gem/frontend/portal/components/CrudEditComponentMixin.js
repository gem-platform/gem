function property(prop) {
  return {
    [prop.name]: {
      get() {
        // get value of specified property from entity
        const value = this.entity[prop.name];

        // entity should be fetched from specified collection
        if (prop.collection) {
          const entities = this.$store.getters[`dashboard/${prop.collection}/keyed`];
          return entities[value];
        }

        // return plain value otherwise
        return value;
      },
      async set(value) {
        // entity is from collection
        if (prop.collection) {
          // fetch entity if ID provided
          if (value && value._id) {
            await this.$store.dispatch(`dashboard/${prop.collection}/fetchOne`, value._id);
          }

          // update entity with specified ID
          this.update({ [prop.name]: value ? value._id : undefined });
        } else {
          // update entity with plain value
          this.update({ [prop.name]: value });
        }

        // update validation info
        if (Object.prototype.hasOwnProperty.call(this, '$v')) {
          this.$v[prop.name].$touch();
        }
      }
    }
  };
}

export default (options) => {
  const result = {};

  // go through all the properties and
  // generate the necessary fields.
  options.properties.forEach((prop) => {
    if (typeof prop === 'string') {
      const o = { name: prop };
      result[o.name] = property(o)[o.name];
    } else if (typeof prop === 'object') {
      result[prop.name] = property(prop)[prop.name];
    } else {
      throw Error('Invalid option');
    }
  });

  return {
    computed: {
      ...result
    },
    methods: {
      update(data) {
        const { entities } = this.$route.params;
        this.$store.dispatch(`dashboard/${entities}/update`, { _id: this.entity._id, ...data });
      }
    }
  };
};
