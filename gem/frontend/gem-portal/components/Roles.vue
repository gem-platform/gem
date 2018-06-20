<template>
  <div>
    <b-taginput
      v-model="roles"
      :data="suggestions"
      autocomplete
      field="name"
      icon="fas fa-angle-right"
      placeholder="Roles"
      @typing="getFilteredRoles" />
  </div>
</template>

<script>
import str from '@/lib/string';

export default {
  props: {
    selected: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      roles: [],
      suggestions: []
    };
  },
  async beforeCreate() {
    await this.$store.dispatch('dashboard/roles/fetch');
    this.roles = this.$store.state.dashboard.roles.roles.filter(r => this.selected.includes(r._id));
  },
  methods: {
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

<style>

</style>
