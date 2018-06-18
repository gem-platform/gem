<template>
  <div>
    <div
      class="speaker-block has-text-centered">
      <div class="is-uppercase is-size-1">
        {{ speaker }}
      </div>
      <p class="heading">Speaking now</p>
    </div>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'DiscussionStageView',
  mixins: [StageStateMixin],
  computed: {
    speaker() {
      const { speaker } = this.$stage;
      const users = this.$store.getters['meeting/users'];
      return (users[speaker] && users[speaker].name) || '-';
    }
  }
};
</script>

<style scoped>
.speaker-name {
  font-size: 350%;
}
</style>

<style scoped>
.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all .8s ease;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
</style>
