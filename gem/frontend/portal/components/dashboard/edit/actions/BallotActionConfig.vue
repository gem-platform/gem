<template>
  <div>
    <b-field label="Threshold">
      <b-checkbox
        v-model="enableThreshold"
        @input="changed">
        Enable threshold
      </b-checkbox>
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
      enableThreshold: this.value.enableThreshold || false
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        enableThreshold: this.enableThreshold
      });
    }
  }
};
</script>
