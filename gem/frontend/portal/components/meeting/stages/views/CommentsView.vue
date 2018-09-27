<template>
  <div>
    <CommentsList :filter="!isPresenter"/>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';

import CommentsList from '@/components/meeting/stages/widgets/CommentsList.vue';

export default {
  name: 'CommentsStageView',
  components: { CommentsList },
  mixins: [AuthMixin],
  computed: {
    /**
     * Is user presenter?
     */
    isPresenter() {
      return this.haveScope('meeting.presenter');
    }
  }
};
</script>
