<template>
  <b-table
    :data="comments"
    :columns="columns"/>
</template>

<script>
export default {
  name: 'CommentsStageView',

  computed: {
    comments() {
      const { meetingStageState } = this.$store.getters;
      return meetingStageState.comments;
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
