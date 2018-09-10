<template>
  <div>
    <div
      v-for="(official, idx) in officials"
      :key="officials[idx] ? officials[idx]._id : idx"
      class="field">

      <b-field grouped>
        <Autocomplete
          :value="officials[idx] ? officials[idx].name : ''"
          :fields="['_id']"
          icon="fas fa-angle-double-right"
          field="name"
          collection="workflowStages"
          placeholder="Type to search"
          @select="selected($event, idx)"/>

        <p class="control">
          <button class="button">
            <span class="icon">
              <i
                class="fa fa-trash"
                @click="remove(idx)"/>
            </span>
          </button>
        </p>
      </b-field>
    </div>

    <a
      class="button is-small"
      @click="add">Add</a>
  </div>
</template>

<script>
import Vue from 'vue';
import Autocomplete from '@/components/Autocomplete.vue';

export default {
  components: { Autocomplete },
  props: {
    /**
     * List of selected official IDs
     * example: [123, 111, 999]
     */
    value: {
      type: Array,
      default() { return []; }
    }
  },
  data() {
    const officials = this.$store.getters['dashboard/workflowStages/keyed'];

    return {
      officials: this.value ? this.value.map(id => officials[id]) : []
    };
  },
  computed: {
    /**
     * Get list of all selected officials
     */
    selectedIds() {
      return this.officials
        .filter(x => x !== undefined)
        .map(x => x._id);
    },

    /**
     * Are all fields filled with officials?
     */
    allFilled() {
      return this.officials.filter(x => x === undefined).length <= 0;
    }
  },
  watch: {
    selectedIds() {
      this.$emit('input', this.selectedIds);
    },
    allFilled(value) {
      // All fields with officials are filled, so add extra one
      if (value) { this.officials.push(undefined); }
    }
  },
  methods: {
    /**
     * Add empty field
     */
    add() {
      this.officials.push(undefined);
    },

    /**
     * Remove using specified index
     */
    remove(index) {
      this.officials = this.officials.filter((r, idx) => idx !== index);
    },

    /**
     * On official is selected
     */
    selected(value, index) {
      Vue.set(this.officials, index, value ? { _id: value._id, name: value.name } : undefined);
    }
  }
};
</script>
