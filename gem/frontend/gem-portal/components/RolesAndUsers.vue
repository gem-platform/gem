<template>
  <b-taginput
    v-model="internalValue"
    :data="usersAndRoles"
    field="name"
    autocomplete
    icon="fas fa-angle-right"
    placeholder="Add a user or role"
    @typing="onTyping">
    <template slot="empty">
      There are no items
    </template>
  </b-taginput>
</template>

<script>
import str from '@/lib/string';

export default {
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      internalValue: this.value,
      usersAndRoles: []
    };
  },
  watch: {
    internalValue(val) {
      this.$emit('input', val);
    }
  },
  async beforeCreate() {
    await this.$store.dispatch('dashboard/roles/fetch');
    await this.$store.dispatch('dashboard/users/fetch');
  },
  methods: {
    onTyping(text) {
      const { roles } = this.$store.state.dashboard.roles;
      const { users } = this.$store.state.dashboard.users;

      const _users = users
        .filter(user => str.contains(user.name, text))
        .map(user => ({
          _id: user._id,
          name: user.name,
          type: 'user'
        }));

      const _roles = roles
        .filter(role => str.contains(role.name, text))
        .map(x => ({
          _id: x._id,
          name: x.name,
          type: 'role'
        }));

      this.usersAndRoles = [
        ..._roles,
        ..._users
      ];
    }
  }
};
</script>
