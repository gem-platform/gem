export default {
  state: {
    connection: {
      success: undefined,
      message: undefined
    },
    handshake: {
      success: undefined,
      message: undefined
    }
  },
  mutations: {
    setConnectionState(state, value) {
      state.connection.success = value;
    },
    setConnectionMessage(state, value) {
      state.connection.message = value;
    },
    setHandshakeState(state, value) {
      state.handshake.success = value;
    },
    setHandshakeMessage(state, value) {
      state.handshake.message = value;
    }
  },
  actions: {
    setHandshakeState(context, data) {
      context.commit('setHandshakeState', data.success);
      context.commit('setHandshakeMessage', data.message);
    },
    setConnectionState(context, data) {
      context.commit('setConnectionState', data.connected);
      context.commit('setConnectionMessage', data.message);
    }
  },
  getters: {
    connection(state) {
      return state.connection;
    },
    handshake(state) {
      return state.handshake;
    }
  }
};
