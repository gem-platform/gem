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
        const { entities } = this.$route.params;
        this.$store.dispatch(`dashboard/${entities}/update`, { _id: this.entity._id, ...data });
      }
    }
  };
};
