<template>
  <div
    class="field">
    <p class="control is-expanded">
      <a
        :class="{ 'is-success' : readState, 'is-white': !!readState }"
        class="button is-fullwidth"
        @click="haveRead">
        I read
      </a>
    </p>
  </div>
</template>

<script>
import com from '@/communication';

export default {
  name: 'AcquaintanceStageControls',
  data() {
    return {
      readState: false
    };
  },
  methods: {
    async haveRead() {
      const r = await com.request({ command: 'have_read' });
      this.readState = r.success;
    }
  }
};
</script>
