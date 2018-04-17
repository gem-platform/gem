export const state = () => ({
  busy: false
});

export const mutations = {
  setBusy(state, value) {
    state.busy = value;
  }
};

export const actions = {
  busy({ commit }, data) {
    commit('setBusy', data);
  }
};

export const getters = {
  busy(state) {
    return state.busy;
  }
};
