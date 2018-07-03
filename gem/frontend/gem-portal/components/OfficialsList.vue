<template>
  <div>
    <div
      v-for="(official, idx) in officials"
      :key="idx"
      class="field">
      <Autocomplete
        :fields="['_id', 'appendage', 'formOfAddress']"
        icon="fas fa-user"
        field="name"
        collection="officials"
        placeholder="Type name to search"/>
    </div>

    <a
      class="button"
      @click="onAddButtonClicked">Add</a>
  </div>
</template>

<script>
import Autocomplete from '@/components/Autocomplete.vue';

export default {
  components: { Autocomplete },
  data() {
    return {
      officials: [1, 2, 3]
    };
  },
  methods: {
    onAddButtonClicked() {
      this.officials.push([]);
    }
  }
};
</script>

<style>

</style>
