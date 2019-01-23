<template>
  <div>
    <b-field label="Proposal display mode">
      <b-select
        v-model="proposalDisplayMode"
        placeholder="Proposal display mode"
        expanded
        @input="changed">
        <option value="full">Entirely</option>
        <option value="in-parts">In parts</option>
      </b-select>
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
      proposalDisplayMode: this.value.proposalDisplayMode || 'in-parts'
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        proposalDisplayMode: this.proposalDisplayMode
      });
    }
  }
};
</script>
