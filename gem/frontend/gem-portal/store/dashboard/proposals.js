export const state = () => ({
  proposals: []
});

export const mutations = {
  set(state, value) {
    state.proposals = value;
  },
  update(state, value) {
    const proposal = state.proposals.find(i => i._id == value._id);
    Object.assign(proposal, value);
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
  },
  async update({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$put('/api/proposal/' + data._id, data);
    commit('update', data);

    commit('setBusy', false, { root: true });
  },
  async create({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$post('/api/proposal', data);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  },
  async remove({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$delete('/api/proposal/' + data.id);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  }
};

export const getters = {
  all(state) {
    return state.proposals;
  },
  get(state) {
    return index =>
      state.proposals.filter(item => {
        return item._id == index;
      });
  }
};
