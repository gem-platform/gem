export default {
  state: {
    stageIndex: -1, // current stage number
    stages: {}, // stages states keyed by index
    proposals: {}, // proposals keyed by proposalId
    users: {}, // list of users keyed by Id
    roles: {}
  },
  mutations: {
    setStageIndex(state, index) {
      state.stageIndex = index;
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
    }
  },
  actions: {
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
    }
  },
  getters: {
    meetingStageType(state) {
      // meeting state is not received yet,
      // so display ConnectedStage
      if (state.stageIndex < 0) {
        return 'ConnectedStage';
      }

      // we have meeting state, so get type of stages
      // by meetingStageIndex
      const { stageIndex, stages } = state;
      return stages[stageIndex].type;
    },
    meetingStageState(state) {
      const idx = state.stageIndex;
      return state.stages[idx];
    },
    stageIndex(state) {
      return state.stageIndex;
    },
    proposal(state) {
      // no meeting info received yet
      if (!state.stages || !state.proposals) {
        return undefined;
      }

      const { stageIndex } = state;
      const stage = state.stages[stageIndex];
      const { proposalId } = stage;

      if (!proposalId) {
        return undefined;
      }

      return state.proposals[proposalId];
    },
    users(state) {
      return state.users;
    },
    user(state) {
      return state.user;
    },
    roles(state) {
      return state.roles;
    }
  }
};
