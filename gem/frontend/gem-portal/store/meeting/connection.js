export const state = () => ({
  state: 'connecting',
  message: ''
});

export const mutations = {
  setConnectionState(state, value) {
    state.state = value.state;
    state.message = value.message;
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
