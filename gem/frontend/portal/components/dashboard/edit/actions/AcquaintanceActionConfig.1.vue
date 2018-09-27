<template>
  <div>
    <b-switch
      v-model="parts"
      @input="changed">
      Show proposal in parts
    </b-switch>
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
      parts: this.value.parts || false
    };
  },
  methods: {
    changed() {
      this.$emit('change', { parts: this.parts });
    }
  }
};
</script>
