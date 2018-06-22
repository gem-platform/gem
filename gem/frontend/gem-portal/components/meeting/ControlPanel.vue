<template>
  <div>
    <p class="heading has-text-centered">Change meeting stage</p>
    <div class="field is-grouped is-grouped-multiline">
      <!-- "Previous stage" button -->
      <p class="control">
        <a
          :disabled="prevDisabled"
          class="button"
          @click="move(-1)">Prev</a>
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

    <p class="heading has-text-centered">Set stage timer</p>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <a
          class="button"
          @click="setStageTime(60)">1 min</a>
      </p>
      <p class="control is-expanded">
        <a
          class="button is-fullwidth"
          @click="setStageTime(120)">2 min</a>
      </p>
      <p class="control">
        <a
          class="button"
          @click="setStageTime(180)">3 min</a>
      </p>
      <p class="control">
        <a
          class="button"
          @click="setStageTime(300)">5 min</a>
      </p>
    </div>
  </div>
</template>

<script>
import com from '@/lib/communication';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import NotificationMixin from '@/components/NotificationMixin';

export default {
  name: 'ControlPanel',
  mixins: [StageStateMixin, NotificationMixin],
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
    },

    /**
     * Add stage time using specified seconds
     */
    async setStageTime(seconds) {
      const res = await com.send('stage_timer', { value: seconds });
      this.notify(
        res.success ? 'Time has been successfully updated' : res.message,
        res.success ? 'is-success' : 'is-danger'
      );
    }
  }
};
</script>
