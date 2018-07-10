import Vue from 'vue';

export const state = () => ({
  names: {}
});

export const mutations = {
  set(state, data) {
    Vue.set(state.names, data.collection, data.items);
  }
};

export const actions = {
  async fetch({ commit }, params) {
    const res = await this.$axios.$get('/api/names', { params });
    commit('set', {
      collection: params.collection,
      items: res.items
    });
  }
};

export const getters = {
  get(state) {
    return state.names;
  }
};
