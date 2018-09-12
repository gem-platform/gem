export default (options) => {
  const result = {};


  function store(context, collection) {
    return {
      get(id) {
        const workflows = context.$store.getters[`dashboard/${collection}/keyed`];
        return workflows[id];
      },
      update(id, data) {
        context.$store.dispatch(`dashboard/${collection}/update`, { _id: id, ...data });
      },
      async fetch(id) {
        await context.$store.dispatch(`dashboard/${collection}/fetchOne`, id);
      }
    };
  }

  // eslint-disable-next-line
  options.forEach(function a(prop) {
    result[prop.name || `$${prop.collection}Store`] = function s() {
      return store(this, prop.collection);
    };
  });

  return {
    computed: {
      ...result
    }
  };
};

