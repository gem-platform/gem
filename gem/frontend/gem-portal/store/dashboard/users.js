export const state = () => ({
  users: []
});

export const mutations = {
  set(state, value) {
    state.users = value;
  },
  update(state, value) {
    const proposal = state.users.find(i => i._id === value._id);
    Object.assign(proposal, value);
  }
};

export const actions = {
  async fetch({ commit }, data) {
    if (!data) {
      const res = await this.$axios.$get('/api/users');
      commit('set', res._items);
    } else {
      const res = await this.$axios.$get(`/api/users?where=${JSON.stringify(data)}`);
      commit('set', res._items);
    }
  },
  async update({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$put(`/api/users/${data._id}`, data);
    commit('update', data);

    commit('setBusy', false, { root: true });
  },
  async create({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$post('/api/users', data);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  },
  async remove({ commit }, data) {
    commit('setBusy', true, { root: true });

    await this.$axios.$delete(`/api/users/${data.id}`);

    commit('setBusy', false, { root: true });
    // commit('create', data);
  }
};

export const getters = {
  all(state) {
    return state.users;
  },
  get(state) {
    return index => state.users.filter(item => item._id === index);
  }
};
