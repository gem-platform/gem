<template>
  <div
    :class="{'overdue': isOverdue,
             'running-out': isRunningOut}"
    class="color-transition">
    <p class="heading">{{ timerHeader }}</p>
    <p class="title time">{{ value }}</p>
  </div>
</template>

<script>
import time from '@/lib/time';

export default {
  props: {
    /**
     * Header of the timer
     */
    header: {
      type: String,
      required: true
    },

    /**
     * Countdown to
     */
    to: {
      type: Date,
      required: true
    }
  },
  data() {
    return {
      diff: undefined
    };
  },
  timers: {
    countdown: { time: 1000, autostart: true, repeat: true }
  },
  computed: {
    /**
     * Is overdue
     */
    isOverdue() {
      return this.diff ? this.diff.negative : false;
    },

    /**
     * Is running out
     */
    isRunningOut() {
      const secondsToWarn = 45;
      return !!(this.diff && !this.diff.negative && this.diff.distance < secondsToWarn * 1000);
    },

    /**
     * Timer header
     */
    timerHeader() {
      const overdue = 'overdue';
      return this.diff && this.diff.negative ? `${this.header} ${overdue}` : this.header;
    },

    /**
     * Timer value
     */
    value() {
      if (this.diff) {
        const s = String(this.diff.seconds).padStart(2, '0');
        const m = String(this.diff.minutes).padStart(2, '0');
        const h = this.diff.hours;
        const d = this.diff.days;

        const result = [];

        if (d) result.push(`${d}d `);
        if (h) result.push(`${h}h `);
        if (m) result.push(`${m}:`);
        if (s) result.push(s);

        return result.join('');
      }
      return '00:00';
    }
  },
  methods: {
    countdown() {
      this.diff = time.diff(new Date(), this.to);
    }
  }
};
</script>

<style>
.time {
  font-feature-settings: "tnum";
}

.color-transition {
  transition: color 1.5s ease;
}

.running-out {
  color: hsl(25, 100%, 60%);
  animation: flash-running-out 1s linear 5;
}
.overdue {
  color: hsl(348, 100%, 61%);
  animation: flash-overdue .5s linear 10;
}

@keyframes flash-running-out {
  50% {
    opacity: .25;
  }
}
@keyframes flash-overdue {
  50% {
    opacity: .25;
  }
}
</style>
