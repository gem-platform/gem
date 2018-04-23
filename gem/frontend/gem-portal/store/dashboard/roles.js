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
    await this.$axios.$put(`/api/roles/${data._id}`, data);
    commit('update', data);
  },
  async create(context, data) {
    await this.$axios.$post('/api/roles', data);
  },
  async remove(context, data) {
    await this.$axios.$delete(`/api/roles/${data.id}`);
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
