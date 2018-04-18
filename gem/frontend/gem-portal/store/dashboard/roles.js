export const state = () => ({
  roles: []
});

export const mutations = {
  set(state, value) {
    state.roles = value;
  },
  update(state, value) {
    const proposal = state.roles.find(i => i._id === value._id);
    Object.assign(proposal, value);
  }
};

export const actions = {
  async fetch({ commit }, data) {
    if (!data) {
      const res = await this.$axios.$get('/api/roles');
      commit('set', res._items);
    } else {
      const res = await this.$axios.$get(`/api/roles?where=${JSON.stringify(data)}`);
      commit('set', res._items);
    }
  },
  async update({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$put(`/api/roles/${data._id}`, data);
    commit('update', data);

    commit('setBusy', false, { root: true });
  },
  async create({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$post('/api/roles', data);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  },
  async remove({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$delete(`/api/roles/${data.id}`);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  }
};

export const getters = {
  all(state) {
    return state.roles;
  },
  get(state) {
    return index => state.roles.filter(item => item._id === index);
  }
};
