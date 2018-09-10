/**
 * Sore to keep status of meetings
 */

export const state = () => ({
  active: [], // list of active meeting ids: [111, 222, 333]
  online: {} // number of users online: { meetingId: number }
});

export const mutations = {
  /**
   * Set active meetings
   * @param {Object} state State of the store
   * @param {Array} value List of active meeting ids
   */
  setActiveMeetings(state, value) {
    state.active = value;
  },
  /**
   * Set number of users online
   * @param {Object} state State of the store
   * @param {Object} value Number of users online keyed by meeting id
   */
  setUsersOnlineCount(state, value) {
    state.online = value;
  }
};

export const actions = {
  /**
   * Sets status of meetings
   * @param {Object} param0 Vuex methods
   * @param {Object} data Status data
   */
  set({
    commit
  }, data) {
    commit('setActiveMeetings', data.active);
    commit('setUsersOnlineCount', data.online);
  }
};

export const getters = {
  /**
   * Return list of active meeting ids
   * @param {Object} state State of the store
   */
  active(state) {
    return state.active;
  },

  /**
   * Return number of users online keyed by meeting id
   * @param {Object} state State of the store
   */
  online(state) {
    return state.online;
  }
};
