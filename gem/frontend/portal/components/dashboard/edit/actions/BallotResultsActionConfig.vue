<template>
  <div>
    <b-field label="Result">
      <b-checkbox
        v-model="showResult"
        @input="changed">
        Show result
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
      showResult: this.value.showResult || false
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        showResult: this.showResult
      });
    }
  }
};
</script>
