<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <b-field label="Permissions">
      <b-taginput
        v-model="value"
        :data="filteredPermissions"
        field="name"
        autocomplete
        icon="fas fa-key"
        placeholder="Add a permission"
        @typing="onPermissionsTyping"
        @input="onPermissionsInput">
        <template slot-scope="props">
          <strong>{{ props.option.name }}</strong>: {{ props.option.desc }}
        </template>
        <template slot="empty">
          There are no items
        </template>
      </b-taginput>
    </b-field>
  </div>
</template>

<script>
import str from '@/lib/string';

export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      value: [],
      permissions: [
        { _id: '*', name: 'Superuser', desc: 'Have full rights' },
        { _id: 'dashboard', name: 'Access Dashboard', desc: 'Access Dashboard page' },
        { _id: 'dashboard.roles', name: 'Access Roles', desc: 'Access Roles page at dashboard' },
        { _id: 'dashboard.proposals', name: 'Access Proposals', desc: 'Access Proposals page at dashboard' },
        { _id: 'dashboard.users', name: 'Access Users', desc: 'Access Users page at dashboard' },
        { _id: 'dashboard.meetings', name: 'Access Meetings', desc: 'Access Meetings page at dashboard' },
        { _id: 'dashboard.laws', name: 'Access Laws', desc: 'Access Laws page at dashboard' },
        { _id: 'meeting', name: 'Access Meetings', desc: 'Access Meeting page' },
        { _id: 'meeting.vote', name: 'Vote' },
        { _id: 'meeting.comment', name: 'Comment' },
        { _id: 'meeting.discuss', name: 'Discuss' },
        { _id: 'meeting.join', name: 'Join Meeting' },
        { _id: 'meeting.manage', name: 'Manage Meeting' }
      ],
      filteredPermissions: []
    };
  },
  async created() {
    this.value = this.permissions.filter(x => this.entity.permissions.includes(x._id));
  },
  methods: {
    onPermissionsTyping(text) {
      // get permissions what contains specified text in names
      // and filter out permissions what already been added
      this.filteredPermissions = this.permissions
        .filter(option => str.contains(option.name, text))
        .filter(option => !this.value.map(x => x._id).includes(option._id));
    },
    onPermissionsInput(value) {
      this.entity.permissions = value.map(x => x._id);
    }
  }
};
</script>
