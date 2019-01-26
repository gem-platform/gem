<template>
  <div>
    <!-- User's name -->
    <b-field label="Name">
      <b-input
        v-model="name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <!-- User's email -->
    <b-field label="Email">
      <b-input
        v-model="email"
        placeholder="Email"/>
    </b-field>

    <!-- Users password -->
    <b-field label="Password">
      <b-input
        v-model="password"
        placeholder="Password"/>
    </b-field>

    <!-- Users roles -->
    <b-field label="Roles">
      <b-taginput
        v-model="roles"
        :data="filteredRoles"
        field="name"
        autocomplete
        icon="fas fa-user"
        placeholder="Add a role"
        @typing="onRolesTyping">
        <template slot="empty">
          There are no items
        </template>
      </b-taginput>
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';
import str from '@/lib/string';

export default {
  mixins: [
    CrudEditComponentMixin({
      properties: [
        'name',
        'email',
        'password'
      ]
    })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      filteredRoles: []
    };
  },
  computed: {
    roles: {
      get() {
        const roles = this.entity.roles || [];
        return roles.map(x => this.rolesList.find(y => y._id === x));
      },
      set(roles) {
        if (this.entity._id === undefined) {
          Object.assign(this.entity, { roles: roles.map(x => x._id) });
          return; // creating new entity. it is not in store yet
        }

        this.$store.dispatch('dashboard/users/update', {
          _id: this.entity._id, roles: roles.map(x => x._id)
        });
      }
    },
    rolesList() {
      const list = this.$store.getters['names/get'].roles;
      return Object.keys(list).map(_id => ({ _id, name: list[_id] }));
    }
  },
  methods: {
    onRolesTyping(text) {
      // get roles what contains specified text in names
      // and filter out roles what already been added
      this.filteredRoles = this.rolesList
        .filter(option => str.contains(option.name, text))
        .filter(option => !this.roles.map(x => x._id).includes(option._id));
    }
  },
  async fetch({ store }) {
    await store.dispatch('names/fetch', {
      collection: 'roles', field: 'name'
    });
  }
};
</script>
