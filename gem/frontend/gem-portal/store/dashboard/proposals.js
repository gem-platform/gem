export const state = () => ({
  proposals: []
});

export const mutations = {
  set(state, value) {
    state.proposals = value;
  }
};

export const actions = {
  async fetch({ commit }) {
    const res = await this.$axios.$get('http://localhost:5000/proposal');
    commit('set', res._items);
  }
};

export const getters = {
  all(state) {
    return state.proposals;
  }
};
