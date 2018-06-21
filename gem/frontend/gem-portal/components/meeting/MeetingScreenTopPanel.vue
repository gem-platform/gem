<template>
  <div class="box notification is-light">
    <div class="level">

      <div class="level-left">
        <div class="level-item">
          <div>
            <p class="heading">{{ subtitle }}</p>
            <p class="title">
              {{ title }}
            </p>
          </div>
        </div>
      </div>

      <div class="level-right">
        <div class="level-item has-text-centered">
          <CountdownTimer
            :to="tillStageEnd"
            header="Stage"/>
        </div>
        <div class="level-item has-text-centered">
          <CountdownTimer
            :to="tillMeetingEnd"
            header="Meeting" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CountdownTimer from '@/components/meeting/CountdownTimer.vue';

export default {
  name: 'MeetingScreenTopPanel',
  components: {
    CountdownTimer
  },
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
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
    tillStageEnd() {
      return this.stageTime;
    },
    tillMeetingEnd() {
      return new Date(this.$store.state.meeting.end);
    }
  },
  mounted() {
    this.$bus.on('setStageTimer', time => this.onUpdateStageTimer(time));
  },
  methods: {
    onUpdateStageTimer(value) {
      this.stageTime = value;
    }
  }
};
</script>
