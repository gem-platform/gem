<template>
  <div>
    <b-taginput
      v-model="selectedRoles"
      :data="suggestions"
      autocomplete
      field="name"
      icon="fas fa-angle-right"
      placeholder="Roles"
      @typing="getFilteredRoles"
      @input="onInput" />
  </div>
</template>

<script>
import str from '@/lib/string';
import arr from '@/lib/array';

export default {
  props: {
    // List of selected role IDs:
    // ['id0', 'id2']
    selected: {
      type: Array,
      required: true
    }
  },
  data() {
    const roles = arr.unkey(this.$store.state.meeting.roles, 'id');

    return {
      // all roles: { id: ..., name: ... }
      roles,

      // list of selected roles
      selectedRoles: roles.filter(x => this.selected.includes(x.id)),

      // list of suggestions
      suggestions: []
    };
  },
  methods: {
    /**
     * On input changed
     */
    onInput(value) {
      // return IDs only
      this.$emit('change', value.map(r => r.id));
    },

    /**
     * Return list of suggestions based on user input
     */
    getFilteredRoles(text) {
      // return list of roles which contains specified text
      this.suggestions = this.roles
        .filter(role => str.contains(role.name, text));
    }
  }
};
</script>
