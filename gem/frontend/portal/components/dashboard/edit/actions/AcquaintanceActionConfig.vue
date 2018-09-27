<template>
  <div>
    <b-field
      label="Proposal display mode">
      <b-switch
        v-model="proposalInParts"
        @input="changed">
        Show proposal in parts
      </b-switch>
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
      proposalInParts: this.value.proposalInParts || false
    };
  },
  methods: {
    changed() {
      this.$emit('change', { proposalInParts: this.proposalInParts });
    }
  }
};
</script>
