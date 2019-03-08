<template>
  <div>
    <b-field
      label="Stage timing">
      <b-input
        v-model="duration"
        placeholder="Duration of the stage in minutes"
        @input="changed"/>
    </b-field>

    <!-- Show stage timer checkbox -->
    <b-checkbox
      v-model="showTimer"
      placeholder="Show stage timer"
      @input="changed">
      Show timer
    </b-checkbox>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Object,
      default() { return {}; }
    }
  },
  data() {
    return {
      duration: this.value.duration,
      showTimer: this.value.showTimer
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        duration: this.duration,
        showTimer: this.showTimer
      });
    }
  }
};
</script>
