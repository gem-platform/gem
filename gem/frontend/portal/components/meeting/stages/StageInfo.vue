<template>
  <div class="box notification is-light">

    <!-- Title and type -->
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <div>
            <!-- Type of a stage -->
            <p
              id="stage-type"
              class="heading">
              {{ type }}
            </p>

            <!-- Title of a stage -->
            <p class="title">
              {{ title }}
            </p>
          </div>
        </div>
      </div>

      <!-- Timers -->
      <div class="level-right">

        <!-- Stage timer -->
        <div
          v-if="stageTimerVisibility"
          class="level-item has-text-centered">
          <CountdownTimer
            :to="stageEndTime"
            header="Stage"/>
        </div>

        <!-- Meeting timer -->
        <div class="level-item has-text-centered">
          <CountdownTimer
            :to="meetingEndTime"
            header="Meeting" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CountdownTimer from '@/components/meeting/CountdownTimer.vue';

export default {
  name: 'StageInfo',
  components: {
    CountdownTimer
  },
  props: {
    /**
     * Title of a stage.
     * Shows proposal title in most cases.
     */
    title: {
      type: String,
      required: true
    },

    /**
     * Type of a stage.
     * For example: "Ballot", "Descussion", "Feedback".
     */
    type: {
      type: String,
      default: ''
    },

    /**
     * Show stage timer.
     * Sometimes it is not required to show stage timer, for example for GEM online.
     */
    showStageTimer: {
      type: Boolean,
      default: true
    },

    /**
     * Stage end time.
     */
    stageEnds: {
      type: Date,
      required: true
    },

    /**
     * Meeting end time.
     */
    meetingEnds: {
      type: Date,
      required: true
    }
  },
  data() {
    return {
      stageEndTime: this.stageEnds,
      meetingEndTime: this.meetingEnds,
      stageTimerVisibility: true
    };
  },
  methods: {
    /**
     * Set stage timer.
     * @param date End date to set to stage timer.
     */
    setStageTimer(date) {
      this.stageEndTime = new Date(date);
    },

    /**
     * Set the stage timer to the specified number of seconds ahead of the current time.
     * @param seconds Time in seconds.
     */
    setStageTimerAhead(seconds) {
      const now = new Date().getTime();
      this.stageEndTime = new Date(now + (seconds * 1000));
    },

    /**
     * Add time to stage timer.
     * @param seconds Time in seconds to add to stage timer.
     */
    addStageTimer(seconds) {
      const current = this.stageEndTime.getTime();
      this.stageEndTime = new Date(current + (seconds * 1000));
    },

    /**
     * Set stage timer visibility.
     * @param value True - show timer, otherwise hide it.
     */
    setStageTimerVisibility(value) {
      this.stageTimerVisibility = value;
    }
  }
};
</script>
