<template>
  <div class="field is-grouped is-grouped-multiline">
    <!-- "Previous stage" button -->
    <p class="control">
      <button
        :disabled="prevDisabled"
        class="button"
        @click="move(-1)">Prev</button>
    </p>

    <!-- "Next stage" button -->
    <p class="control is-expanded">
      <a
        :disabled="nextDisabled"
        class="button is-fullwidth"
        @click="move(1)">
        <span>Next</span>
        <span class="icon">
          <i class="fa fa-angle-right"/>
        </span>
      </a>
    </p>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'ControlPanel',
  mixins: [StageStateMixin],
  computed: {
    /**
     * Disable "Next" button or not?
     */
    nextDisabled() {
      return this.stageIndex >= this.stagesCount - 1;
    },

    /**
     * Disable "Prev" button or not?
     */
    prevDisabled() {
      return this.stageIndex <= 0;
    }
  },
  methods: {
    /**
     * Move to next stage
     */
    move(step) {
      const nextStageIndex = this.stageIndex + step;
      this.$socket.emit('switch_stage', { index: nextStageIndex });
    }
  }
};
</script>
