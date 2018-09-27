export const state = () => ({
  id: 0,
  stageIndex: -1, // current stage number
  stages: {}, // stages states keyed by index
  proposals: {}, // proposals keyed by proposalId
  users: {}, // list of users keyed by Id
  roles: {},
  start: undefined,
  end: undefined,
  attentionRequired: false,
  closed: false
});

export const mutations = {
  setId(state, data) {
    state.id = data;
  },
  setStageIndex(state, index) {
    state.stageIndex = index || 0;
  },
  setStageState(state, data) {
    state.stages[data.index] = data.state;
  },
  setMeetingStages(state, data) {
    state.stages = data;
  },
  setProposals(state, proposals) {
    state.proposals = proposals;
  },
  setMeetingUsers(state, users) {
    state.users = users;
  },
  setMeetingRoles(state, roles) {
    state.roles = roles;
  },
  setUserData(state, data) {
    state.user = data;
  },
  setAttentionRequired(state, value) {
    state.attentionRequired = value;
  },
  setMeetingStart(state, value) {
    state.start = value;
  },
  setMeetingEnd(state, value) {
    state.end = value;
  },
  setClose(state, value) {
    state.closed = value;
  }
};

export const actions = {
  meetingId(context, data) {
    context.commit('setId', data);
  },
  meetingStage(context, data) {
    context.commit('setStageState', data);

    // stage index is not changes, so do not call
    // setStageIndex unnecessary
    if (data.index !== context.state.stageIndex) {
      context.commit('setStageIndex', data.index);
    }
  },
  meetingState(context, data) {
    context.commit('setMeetingRoles', data.roles);
    context.commit('setMeetingUsers', data.users);
    context.commit('setMeetingStages', data.stages.list);
    context.commit('setProposals', data.proposals);
    context.commit('setStageIndex', data.stages.index);
    context.commit('setMeetingStart', data.start);
    context.commit('setMeetingEnd', data.end);
  },
  attentionRequired({ commit }, value) {
    commit('setAttentionRequired', value);
  },
  close({ commit }, value) {
    commit('setClose', value);
  }
};

export const getters = {
  users(state) {
    return state.users;
  },
  roles(state) {
    return state.roles;
  },
  attentionRequired(state) {
    return state.attentionRequired;
  }
};
