<template>
  <component :is="componentType"/>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import AgendaView from './stages/views/AgendaView.vue';
import AcquaintanceView from './stages/views/AcquaintanceView.vue';
import ConnectedView from './stages/views/ConnectedView.vue';
import BallotView from './stages/views/BallotView.vue';
import BallotResultsView from './stages/views/BallotResultsView.vue';
import CommentsView from './stages/views/CommentsView.vue';
import DiscussionView from './stages/views/DiscussionView.vue';
import FinalView from './stages/views/FinalView.vue';

export default {
  name: 'StageViewPresenter',
  components: {
    AgendaView,
    ConnectedView,
    AcquaintanceView,
    BallotView,
    BallotResultsView,
    CommentsView,
    DiscussionView,
    FinalView
  },
  mixins: [StageStateMixin],
  computed: {
    /**
     * Return component type to render
     */
    componentType() {
      const shortType = this.stageType.replace('Stage', '');
      return `${shortType}View`;
    }
  }
};
</script>
