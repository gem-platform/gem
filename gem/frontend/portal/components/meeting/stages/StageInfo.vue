<template>
  <div class="box notification is-light">

    <!-- Title and type -->
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <div>
            <p
              id="stage-type"
              class="heading">
              {{ type }}
            </p>
            <p class="title">
              {{ title }}
            </p>
          </div>
        </div>
      </div>

      <!-- Timers -->
      <div class="level-right">

        <!-- Stage timer -->
        <div class="level-item has-text-centered">
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
import StageMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'StageInfo',
  components: {
    CountdownTimer
  },
  mixins: [StageMixin],
  props: {
    title: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      stageTime: new Date()
    };
  },
  computed: {
    /**
     * Return end time of the stage
     */
    stageEndTime() {
      return this.stageTime;
    },

    /**
     * Return end time of the meeting
     */
    meetingEndTime() {
      return new Date(this.meetingTime.end);
    }
  },
  mounted() {
    this.$bus.on('setStageTimer', time => this.onSetStageTimer(time));
    this.$bus.on('addStageTimer', time => this.onAddStageTimer(time));
  },
  beforeDestroy() {
    this.$bus.off('setStageTimer');
  },
  methods: {
    onSetStageTimer(value) {
      this.stageTime = value;
    },
    onAddStageTimer(value) {
      this.stageTime = new Date(this.stageTime.getTime() + (1000 * (value || 0)));
    }
  }
};
</script>
