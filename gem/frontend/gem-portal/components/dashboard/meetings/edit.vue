<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.title"
        placeholder="Title"
        size="is-large"/>
    </b-field>

    <b-field label="Agenda">
      <b-input
        v-model="entity.agenda"
        type="textarea"
        placeholder="Agenda"/>
    </b-field>

    <b-field label="Join permissions">
      <RolesAndUsers
        v-model="joinPermissions"
        @input="test"/>
    </b-field>

    <b-field label="Vote permissions">
      <RolesAndUsers
        v-model="votePermissions"
        @input="test"/>
    </b-field>
  </div>
</template>

<script>
import RolesAndUsers from '@/components/RolesAndUsers.vue';

export default {
  components: { RolesAndUsers },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      joinPermissions: this.getPermissions('meeting.join'),
      votePermissions: this.getPermissions('meeting.vote')
    };
  },
  methods: {
    test() {
      this.entity.permissions = [].concat(
        this.joinPermissions.map(x => ({
          scope: 'meeting.join',
          user: x.type === 'user' ? x._id : undefined,
          role: x.type === 'role' ? x._id : undefined
        })),
        this.votePermissions.map(x => ({
          scope: 'meeting.vote',
          user: x.type === 'user' ? x._id : undefined,
          role: x.type === 'role' ? x._id : undefined
        }))
      );
    },
    getPermissions(perm) {
      const allRoles = this.$store.getters['dashboard/roles/all'];
      const allUsers = this.$store.getters['dashboard/users/all'];

      return this.entity.permissions
        .filter(x => x.scope === perm)
        .map(p => ({
          _id: p.role || p.user,
          type: p.role ? 'role' : 'user',
          name: p.role ?
            allRoles.find(x => x._id === p.role).name :
            allUsers.find(x => x._id === p.user).name
        }));
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/roles/fetch');
    await store.dispatch('dashboard/users/fetch');
  }
};
</script>
