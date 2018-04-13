export const state = () => ({
  proposals: []
});

export const mutations = {
  set(state, value) {
    state.proposals = value;
  }
};

export const actions = {
  async fetch({ commit }, data) {
    if (!data) {
      const res = await this.$axios.$get('/api/proposal');
      commit('set', res._items);
    } else {
      const res = await this.$axios.$get(
        '/api/proposal?where=' + JSON.stringify(data)
      );
      commit('set', res._items);
    }
  }
};

export const getters = {
  all(state) {
    return state.proposals;
  },
  get(state) {
    return index =>
      state.proposals.filter(item => {
        return item.index == index;
      });
  }
};
