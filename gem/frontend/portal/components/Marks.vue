<template>
  <div>
    <b-taginput
      v-model="selected"
      :data="marks"
      autocomplete
      field="name"
      icon="fas fa-angle-right"
      placeholder="Marks"
      @input="onInput" />
  </div>
</template>

<script>
export default {
  data() {
    const marks = [
      { name: 'Plus', value: '+' },
      { name: 'Minus', value: '-' },
      { name: 'Info', value: 'i' }
    ];

    return {
      selected: marks.slice(),
      marks
    };
  },
  methods: {
    onInput(value) {
      this.$emit('change', value.map(x => x.value));
    }
  }
};
</script>
