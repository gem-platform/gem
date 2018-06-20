export default (options) => {
  const apiPath = `/api/${options.name}` || options.api;

  return {
    state: () => ({
      [options.name]: []
    }),
    mutations: {
      set(state, value) {
        value.forEach((x) => {
          delete x._created;
          delete x._updated;
          delete x._links;

          const proposal = state[options.name].find(y => y._id === x._id);
          if (proposal) {
            Object.assign(proposal, x);
          } else {
            state[options.name].push(x);
          }
        });
      },
      unset(state, value) {
        value.forEach((x) => {
          state[options.name] = state[options.name].filter(y => y._id !== x._id);
        });
      }
    },
    actions: {
      async fetch({ commit }, data) {
        if (!data) {
          const res = await this.$axios.$get(apiPath);
          commit('set', res._items);
        } else {
          const res = await this.$axios.$get(`${apiPath}?where=${JSON.stringify(data)}`);
          commit('set', res._items);
        }
      },
      async update({ commit }, data) {
        await this.$axios.$put(`${apiPath}/${data._id}`, data);
        commit('set', [data]);
      },
      async mutate({ state, commit }, data) {
        commit('set', [data]);
        const proposal = state[options.name].find(y => y._id === data._id);
        if (proposal) {
          await this.$axios.$put(`${apiPath}/${data._id}`, proposal);
        }
      },
      async create(context, data) {
        await this.$axios.$post(apiPath, data);
      },
      async remove({ commit }, data) {
        await this.$axios.$delete(`${apiPath}/${data.id}`);
        commit('unset', [{ _id: data.id }]);
      }
    },
    getters: {
      all(state) {
        return state[options.name];
      },
      get(state) {
        return index => state[options.name].filter(item => item._id === index);
      }
    }
  };
};

