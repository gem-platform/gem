import User from '@/lib/user.js';

export const getters = {
  type(state, getters, rootState) {
    // meeting state is not received yet,
    // so display ConnectedStage
    if (rootState.meeting.stageIndex < 0) {
      return 'ConnectedStage';
    }

    // we have meeting state, so get type of stages
    // by meetingStageIndex
    const { stageIndex, stages } = rootState.meeting;
    return stages[stageIndex].type;
  },
  state(state, getters, rootState) {
    const idx = rootState.meeting.stageIndex;
    return rootState.meeting.stages[idx];
  },
  index(state, getters, rootState) {
    return rootState.meeting.stageIndex;
  },
  proposal(state, getters, rootState) {
    // no meeting info received yet
    if (
      !rootState.meeting.stages ||
      !rootState.meeting.proposals ||
      rootState.meeting.stageIndex <= -1
    ) {
      return undefined;
    }

    const { stageIndex } = rootState.meeting;
    const stage = rootState.meeting.stages[stageIndex];
    const { proposalId } = stage;

    if (!proposalId) {
      return undefined;
    }

    return rootState.meeting.proposals[proposalId];
  }
};
