<template>
  <div>
    <CommentsList :filter="true"/>
  </div>
</template>

<script>
import CommentsList from '@/components/meeting/stages/widgets/CommentsList.vue';

export default {
  name: 'CommentsStageView',
  components: { CommentsList }
};
</script>
