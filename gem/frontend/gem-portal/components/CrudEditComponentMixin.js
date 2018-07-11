export default (options) => {
  const result = {};

  function property(name) {
    return {
      [name]: {
        get() { return this.entity[name]; },
        set(value) { this.update({ [name]: value }); }
      }
    };
  }

  options.properties.forEach((prop) => {
    result[prop] = property(prop)[prop];
  });

  return {
    computed: {
      ...result
    },
    methods: {
      update(data) {
        if (this.entity._id === undefined) {
          Object.assign(this.entity, data);
          return; // creating new entity. it is not in store yet
        }
        const { entities } = this.$route.params;
        this.$store.dispatch(`dashboard/${entities}/update`, { _id: this.entity._id, ...data });
      }
    }
  };
};
