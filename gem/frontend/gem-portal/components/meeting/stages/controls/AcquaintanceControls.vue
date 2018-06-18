<template>
  <div
    class="field">
    <p class="control is-expanded">
      <a
        :class="{ 'is-success' : readState, 'is-white': !!readState }"
        class="button is-fullwidth">
        I read
      </a>
    </p>
  </div>
</template>

<script>
import com from '@/lib/communication';

export default {
  name: 'AcquaintanceStageControls',
  data() {
    return {
      readState: false,
      readProgress: 0,
      readProgressNext: 0
    };
  },
  created() {
    window.addEventListener('scroll', this.onScroll);
  },
  destroyed() {
    window.removeEventListener('scroll', this.onScroll);
  },
  methods: {
    /**
     * Set reading progress
     */
    async setProgress(quantity) {
      await com.send('have_read', { quantity });
    },

    /**
     * On scroll event
     */
    onScroll() {
      const limit = Math.max(
        document.body.scrollHeight, document.body.offsetHeight,
        document.documentElement.clientHeight, document.documentElement.scrollHeight,
        document.documentElement.offsetHeight
      ) - window.innerHeight;
      const percentRead = window.scrollY / limit;

      if (percentRead > this.readProgressNext || percentRead >= 1) {
        this.readProgress = percentRead;
        this.readProgressNext = percentRead + 0.05;
        this.setProgress(this.readProgress);
        this.readState = percentRead >= 1;
      }
    }
  }
};
</script>
