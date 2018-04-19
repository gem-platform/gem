import User from '@/lib/user';

export const state = () => ({
  stageIndex: -1, // current stage number
  stages: {}, // stages states keyed by index
  proposals: {}, // proposals keyed by proposalId
  users: {}, // list of users keyed by Id
  roles: {},
  user: {},
  attentionRequired: false
});

export const mutations = {
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
  }
};

export const actions = {
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
    context.commit('setStageIndex', data.stages.index);
  },
  meetingProposals(context, data) {
    context.commit('setProposals', data);
  },
  user(context, user) {
    context.commit('setUserData', user);
  },
  attentionRequired({ commit }, value) {
    commit('setAttentionRequired', value);
  }
};

export const getters = {
  users(state) {
    return state.users;
  },
  user(state) {
    return state.user ? new User(state.user) : undefined;
  },
  roles(state) {
    return state.roles;
  },
  attentionRequired(state) {
    return state.attentionRequired;
  }
};
