<template>
  <component :is="componentType"/>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import BallotControls from '@/components/meeting/stages/controls/BallotControls.vue';
import CommentsControls from '@/components/meeting/stages/controls/CommentsControls.vue';
import DiscussionControls from '@/components/meeting/stages/controls/DiscussionControls.vue';
import FinalControls from '@/components/meeting/stages/controls/FinalControls.vue';

export default {
  name: 'StageControlsPresenter',
  components: {
    BallotControls,
    CommentsControls,
    DiscussionControls,
    FinalControls
  },
  mixins: [StageStateMixin],
  computed: {
    /**
     * Return component type to render
     */
    componentType() {
      const shortType = this.stageType.replace('Stage', '');
      return `${shortType}Controls`;
    }
  }
};
</script>
