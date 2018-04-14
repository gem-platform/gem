export const state = () => ({
  connection: {
    success: undefined,
    message: undefined
  },
  handshake: {
    success: undefined,
    message: undefined
  },
  state: false
});

export const mutations = {
  setConnectionState(state, value) {
    state.connection.success = value;
  },
  setConnectionMessage(state, value) {
    state.connection.message = value;
  },
  setHandshakeState(state, value) {
    state.handshake.success = value;
    state.state = value;
  },
  setHandshakeMessage(state, value) {
    state.handshake.message = value;
  }
};

export const actions = {
  setHandshakeState(context, data) {
    context.commit('setHandshakeState', data.success);
    context.commit('setHandshakeMessage', data.message);
  },
  setConnectionState(context, data) {
    context.commit('setConnectionState', data.connected);
    context.commit('setConnectionMessage', data.message);
  }
};

export const getters = {
  connection(state) {
    return state.connection;
  },
  handshake(state) {
    return state.handshake;
  },
  state(state) {
    return state.state;
  }
};
