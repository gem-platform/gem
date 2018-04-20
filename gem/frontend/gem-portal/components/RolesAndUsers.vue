<template>
  <multiselect
    v-model="internalValue"
    :options="options"
    :multiple="true"
    :close-on-select="false"
    :clear-on-select="true"
    :hide-selected="true"
    :group-select="true"
    select-label=""
    group-values="scopes"
    group-label="group"
    placeholder="Roles and users"
    label="name"
    track-by="_id">
    <template
      slot="option"
      slot-scope="props">
      <div class="level">
        <span>{{ props.option.name || props.option.$groupLabel }}</span>
        <span class="has-text-grey role-description">{{ props.option.desc }}</span>
      </div>
    </template>
    <template
      slot="tag"
      slot-scope="props">
      <span
        :class="props.option.type == 'user' ? 'is-info' : 'is-primary'"
        class="tag ctag">
        {{ props.option.name }}
        <button
          class="delete is-small"
          @click.prevent="props.remove(props.option)"/>
      </span>
    </template>
  </multiselect>
</template>

<script>
export default {
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return { internalValue: this.value };
  },
  computed: {
    options() {
      const { roles } = this.$store.state.dashboard.roles;
      const { users } = this.$store.state.dashboard.users;

      const _users = roles
        .map(role => ({
          group: `Users: ${role.name}`,
          scopes: users
            .filter(users => users.roles.includes(role._id))
            .map(user => ({
              _id: user._id,
              name: user.name,
              type: 'user'
            }))
        }));

      const _roles = roles.map(x => ({
        _id: x._id,
        name: x.name,
        type: 'role'
      }));

      return [
        {
          group: 'Roles',
          scopes: _roles
        },
        ..._users
      ];
    }
  },
  watch: {
    internalValue(val) {
      this.$emit('input', val);
    }
  },
  async beforeCreate() {
    await this.$store.dispatch('dashboard/roles/fetch');
    await this.$store.dispatch('dashboard/users/fetch');
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
.ctag {
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>
