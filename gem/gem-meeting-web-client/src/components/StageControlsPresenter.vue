<template>
  <component :is="controlType"/>
</template>

<script>
import AcquaintanceControls from './stages/controls/AcquaintanceControls.vue';
import BallotControls from './stages/controls/BallotControls.vue';
import CommentsControls from './stages/controls/CommentsControls.vue';
import DiscussionControls from './stages/controls/DiscussionControls.vue';

export default {
  name: 'StageControlsPresenter',
  components: {
    AcquaintanceControls,
    BallotControls,
    CommentsControls,
    DiscussionControls,
  },
  computed: {
    controlType() {
      const stage = this.$store.getters.meetingStageType;
      const shortType = stage.replace('Stage', '');
      return `${shortType}Controls`;
    },
  },
};
</script>
