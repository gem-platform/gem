<template>
  <b-taginput
    v-model="internalValue"
    :data="usersAndRoles"
    field="name"
    autocomplete
    icon="fas fa-angle-right"
    placeholder="Add a user or role"
    @typing="typing">
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
  methods: {
    /**
     * On typing
     */
    typing(text) {
      let { roles, users } = this.$store.getters['names/get'];
      roles = Object.keys(roles).map(_id => ({ _id, name: roles[_id] }));
      users = Object.keys(users).map(_id => ({ _id, name: users[_id] }));

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
