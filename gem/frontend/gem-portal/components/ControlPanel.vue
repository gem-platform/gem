<template>
  <div class="field is-grouped is-grouped-multiline">
    <p class="control">
      <a
        class="button"
        @click="move(-1)">Prev</a>
    </p>
    <p class="control is-expanded">
      <a
        class="button is-fullwidth"
        @click="move(1)">Next</a>
    </p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'ControlPanel',
  computed: mapGetters(['meetingStageType']),
  methods: {
    move(step) {
      const stageIndex = this.$store.getters['meeting/stage/index'];
      const nextStageIndex = stageIndex + step;
      this.$socket.emit('switch_stage', { index: nextStageIndex });
      console.log(nextStageIndex);
    }
  }
};
</script>
