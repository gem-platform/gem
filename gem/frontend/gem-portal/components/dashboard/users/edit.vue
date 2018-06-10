<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <b-field label="Password">
      <b-input
        v-model="entity.password"
        placeholder="Password"/>
    </b-field>

    <b-field label="Roles">
      <b-taginput
        v-model="userRoles"
        :data="filteredRoles"
        field="name"
        autocomplete
        icon="fas fa-user"
        placeholder="Add a role"
        @typing="onRolesTyping"
        @input="onRolesInput">
        <template slot="empty">
          There are no items
        </template>
      </b-taginput>
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      userRoles: [],
      filteredRoles: []
    };
  },
  computed: {
    roles() {
      return this.$store.getters['dashboard/roles/all'];
    }
  },
  created() {
    // user have no roles, no additional initialization required
    if (!this.entity.roles) { return; }

    // get all roles
    const roles = this.$store.getters['dashboard/roles/all'];
    this.userRoles = roles.filter(x => this.entity.roles.includes(x._id));
  },
  methods: {
    onRolesTyping(text) {
      this.filteredRoles = this.roles
        .filter(option => option.name
          .toString()
          .toLowerCase()
          .indexOf(text.toLowerCase()) >= 0)
        .filter(option => !this.userRoles.map(x => x._id).includes(option._id));
    },
    onRolesInput(value) {
      this.entity.roles = value.map(x => x._id);
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/roles/fetch');
  }
};
</script>
