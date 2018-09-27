<template>
  <div>
    <b-field
      label="Duration (min)">
      <b-input
        v-model="duration"
        placeholder="Duration of the stage in minutes"
        @input="changed"/>
    </b-field>
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
      duration: this.value.duration
    };
  },
  methods: {
    changed() {
      this.$emit('change', { duration: this.duration });
    }
  }
};
</script>
