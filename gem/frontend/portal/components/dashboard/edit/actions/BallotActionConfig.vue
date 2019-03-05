<template>
  <div>
    <b-field label="Threshold">
      <b-checkbox
        v-model="enableThreshold"
        @input="changed">
        Enable threshold
      </b-checkbox>
    </b-field>
    <b-field label="Quorum">
      <b-checkbox
        v-model="checkQuorum"
        @input="changed">
        Check quorum
      </b-checkbox>
    </b-field>
    <b-field label="Quorum value">
      <b-input
        v-model="quorum"
        placeholder="Quorum value"
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
      enableThreshold: this.value.enableThreshold || false,
      checkQuorum: this.value.checkQuorum || false,
      quorum: this.value.quorum || 19
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        enableThreshold: this.enableThreshold,
        checkQuorum: this.checkQuorum,
        quorum: this.quorum
      });
    }
  }
};
</script>
