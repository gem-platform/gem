<template>
  <div
    class="field">
    <p class="control is-expanded">
      <span
        :class="{ 'is-success' : haveRead, 'is-white': !!haveRead }"
        class="button is-fullwidth">
        I read {{ readProgress | percent }}%
      </span>
    </p>
  </div>
</template>

<script>
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'AcquaintanceStageControls',
  filters: {
    percent(value) {
      return Math.ceil(value * 100);
    }
  },
  mixins: [CommunicationMixin],
  data() {
    return {
      readProgress: 0,
      readProgressNext: 0
    };
  },
  computed: {
    /**
     * Did the user read the document or not?
     */
    haveRead() {
      return this.readProgress >= 1;
    }
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
    setProgress(quantity) {
      this.send('reading_progress', { quantity });
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
      }
    }
  }
};
</script>
