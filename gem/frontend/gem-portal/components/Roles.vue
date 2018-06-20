<template>
  <div>
    <b-taginput
      v-model="roles"
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

export default {
  props: {
    // List of selected roles:
    // ['id0', 'id2']
    selected: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      roles: [], // list of selected roles
      suggestions: [] // list of suggestions
    };
  },
  async beforeCreate() {
    await this.$store.dispatch('dashboard/roles/fetch');
    this.roles = this.$store.state.dashboard.roles.roles.filter(r => this.selected.includes(r._id));
  },
  methods: {
    /**
     * On input changed
     */
    onInput(value) {
      // return IDs only
      this.$emit('change', value.map(r => r._id));
    },

    /**
     * Return list of suggestions based on user input
     */
    getFilteredRoles(text) {
      const { roles } = this.$store.state.dashboard.roles;
      this.suggestions = roles.filter(role => str.contains(role.name, text));
    }
  }
};
</script>
