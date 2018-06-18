<template>
  <b-table
    :data="comments"
    :columns="columns"/>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'CommentsStageView',
  mixins: [StageStateMixin],
  computed: {
    comments() {
      return this.$stage.comments;
    },
    columns() {
      return [
        { field: 'user', label: 'Name' },
        { field: 'content', label: 'Value' },
        { field: 'mark', label: 'Mark', width: '100' }
      ];
    }
  }
};
</script>
