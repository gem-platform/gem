<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.title"
        placeholder="Title"
        size="is-large"/>
    </b-field>

    <b-field label="Select a date">
      <b-datepicker
        v-model="date"
        placeholder="Click to select..."
        icon="fa fa-anchor"
        @input="timeChanged"/>
    </b-field>

    <div class="columns">
      <div class="column">
        <b-field
          label="Start time">
          <b-timepicker
            :readonly="false"
            v-model="startTime"
            placeholder="Type or select a time..."
            icon="fa fa-clock"
            @input="timeChanged"/>
        </b-field>
      </div>

      <div class="column">
        <b-field
          label="End time">
          <b-timepicker
            :readonly="false"
            v-model="endTime"
            placeholder="Type or select a time..."
            icon="fa fa-clock"
            @input="timeChanged"/>
        </b-field>
      </div>
    </div>

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
import time from '@/lib/time';

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
      date: time.stripTime(time.parseIsoDatetime(this.entity.start)),
      startTime: time.parseIsoDatetime(this.entity.start),
      endTime: time.parseIsoDatetime(this.entity.end),
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
    },
    dateChanged() {
    },
    timeChanged() {
      if (this.date && this.startTime && this.endTime) {
        const startDate = time.stripTime(this.date).getTime();
        const startHours = this.startTime.getHours();
        const startMinutes = this.startTime.getMinutes();
        const endHours = this.endTime.getHours();
        const endMinutes = this.endTime.getMinutes();

        this.entity.start = time.toIso(new Date(startDate + (1000 * 60 * 60 * startHours)
          + (1000 * 60 * startMinutes)));
        this.entity.end = time.toIso(new Date(startDate + (1000 * 60 * 60 * endHours)
          + (1000 * 60 * endMinutes)));
      }
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/roles/fetch');
    await store.dispatch('dashboard/users/fetch');
  }
};
</script>
