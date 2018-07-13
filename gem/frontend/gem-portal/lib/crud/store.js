import Vue from 'vue';
import omit from 'lodash/omit';

export default (options) => {
  const api = `/api/${options.collection}`;

  return {
    state: () => ({
      items: {},
      paginated: {},
      total: 0,
      perPage: 0
    }),
    mutations: {
      ...options.mutations,

      meta(state, data) {
        state.total = data.total;
        state.perPage = data.perPage;
      },

      set(state, { entities, page }) {
        entities.forEach((entity) => {
          if (entity._id === undefined) {
            throw Error('Unable to store entity without id');
          }

          Vue.set(state.items, entity._id, entity);
        });

        Vue.set(state.paginated, page, entities);
      },

      unset(state, value) {
        value.forEach((x) => {
          Vue.set(state.items, x._id, undefined);
        });
      },

      update(state, data) {
        Object.assign(state.items[data._id], data);
      }
    },
    actions: {
      /**
       * Fetch one entity by specified id
       * @param {context} param0 Context
       * @param {Number} id Id of object to fetch
       */
      async fetchOne({ commit }, id, params) {
        if (id === undefined) {
          throw Error('Unable to fetch entity: ID is not defined');
        }

        const url = `${api}/${id}`;
        const res = await this.$axios.$get(
          url,
          { params: Object.assign({}, params, options.fetchOneArgs) }
        );

        commit('set', { entities: [res] });
        return res;
      },

      /**
       * Fetch one entity by specified id
       * @param {context} param0 Context
       * @param {Number} id Id of object to fetch
       */
      async fetchList({ commit }, options) {
        if (options.ids === undefined) {
          throw Error('Unable to fetch list: IDs is not defined');
        }
        if (options.ids.length === 0) {
          throw Error('Unable to fetch list: IDs is empty');
        }
        if (options.ids.length > 25) {
          throw Error('Too many items requested. Pagination will cut results to 25');
        }

        const url = `${api}`;
        const res = await this.$axios.$get(
          url,
          { params: { where: { _id: { $in: options.ids } }, ...options.params } }
        );

        commit('set', { entities: res._items });
        return res;
      },

      /**
       * Fetch entities using specified criteria
       * @param {context} param0 Context
       * @param {object} data Filter
       */
      async fetchPage({ commit }, params) {
        const res = await this.$axios.$get(api, { params });
        commit('set', { entities: res._items, page: res._meta.page });
        commit('meta', { total: res._meta.total, perPage: res._meta.max_results });
        return res;
      },

      update({ commit }, data) {
        if (data._id === undefined) {
          throw Error('No _id field provided to update entity');
        }
        commit('update', data);
      },

      async save(_, entity) {
        let data = omit(entity, ['_created', '_updated', '_links']);
        if (options.beforeSave) {
          data = options.beforeSave(data);
        }

        if (entity._id) {
          const url = `${api}/${entity._id}`;
          await this.$axios.$put(url, data);
        } else {
          await this.$axios.$post(api, data);
        }
      },

      async remove({ commit }, data) {
        await this.$axios.$delete(`${api}/${data.id}`);
        commit('unset', [{ _id: data.id }]);
      }
    },

    getters: {
      keyed(state) {
        return state.items;
      },
      list(state) {
        return Object.values(state.items);
      },
      paginated(state) {
        return state.paginated;
      },
      meta(state) {
        return {
          total: state.total,
          perPage: state.perPage
        };
      },
      empty() {
        return () => (options.empty ? options.empty() : {});
      }
    }
  };
};


// export default (options) => {
//   const apiPath = `/api/${options.name}` || options.api;

//   return {
//     state: () => ({
//       [options.name]: []
//     }),
//     mutations: {
//       set(state, value) {
//         value.forEach((x) => {
//           delete x._created;
//           delete x._updated;
//           delete x._links;

//           const proposal = state[options.name].find(y => y._id === x._id);
//           if (proposal) {
//             Object.assign(proposal, x);
//           } else {
//             state[options.name].push(x);
//           }
//         });
//       },
//       unset(state, value) {
//         value.forEach((x) => {
//           state[options.name] = state[options.name].filter(y => y._id !== x._id);
//         });
//       }
//     },
//     actions: {
//       async fetch({ commit }, data) {
//         if (!data) {
//           const res = await this.$axios.$get(apiPath);
//           commit('set', res._items);
//         } else if (data && !data._id) {
//           const res = await this.$axios.$get(`${apiPath}?where=${JSON.stringify(data)}`);
//           commit('set', res._items);
//         } else if (data && data._id) {
//           const res = await this.$axios.$get(`${apiPath}/${data._id}`);
//           commit('set', [res]);
//         }
//       },
//       async update({ commit }, data) {
//         await this.$axios.$put(`${apiPath}/${data._id}`, data);
//         commit('set', [data]);
//       },
//       async mutate({ state, commit }, data) {
//         commit('set', [data]);
//         const proposal = state[options.name].find(y => y._id === data._id);
//         if (proposal) {
//           await this.$axios.$put(`${apiPath}/${data._id}`, proposal);
//         }
//       },
//       async create(context, data) {
//         await this.$axios.$post(apiPath, data);
//       },
//       async remove({ commit }, data) {
//         await this.$axios.$delete(`${apiPath}/${data.id}`);
//         commit('unset', [{ _id: data.id }]);
//       }
//     },
//     getters: {
//       all(state) {
//         return state[options.name];
//       },
//       get(state) {
//         return index => state[options.name].filter(item => item._id === index);
//       }
//     }
//   };
// };

