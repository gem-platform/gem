export default {
  async fetch(store, resources) {
    const promises = [];
    resources.forEach((r) => {
      let promise;
      if (r.one) {
        promise = store.dispatch(`dashboard/${r.resource}/fetchOne`, r.one);
      } else if (r.list) {
        promise = store.dispatch(`dashboard/${r.resource}/fetchList`, r.list);
      }
      promises.push(promise);
    });

    await Promise.all(promises);
  }
};

