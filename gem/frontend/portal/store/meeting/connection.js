export const state = () => ({
  state: 'connecting',
  message: '',
  actions: []
});

export const mutations = {
  setConnectionState(state, value) {
    state.state = value.state;
    state.message = value.message;
    state.actions = value.actions;
  }
};

export const actions = {
  setConnectionState(context, value) {
    context.commit('setConnectionState', value);
  }
};

export const getters = {
  state(state) {
    return state;
  }
};
