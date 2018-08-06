<template>
  <div>
    <!-- Name of the meeting -->
    <b-field label="Name">
      <b-input
        v-model="title"
        placeholder="Title"
        size="is-large"/>
    </b-field>

    <!-- Date and time of the meeting -->
    <b-field label="Select a date">
      <b-datepicker
        v-model="date"
        placeholder="Click to select..."
        icon="calendar"
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
            @input="timeChanged"/>
        </b-field>
      </div>
    </div>

    <!-- Agenda -->
    <b-field label="Agenda">
      <b-input
        v-model="agenda"
        type="textarea"
        placeholder="Agenda"/>
    </b-field>

    <!-- Permissions -->
    <b-field label="Join permissions">
      <RolesAndUsers
        v-model="permissionsJoin"
        @input="test" />
    </b-field>

    <b-field label="Vote permissions">
      <RolesAndUsers
        v-model="permissionsVote"
        @input="test"/>
    </b-field>

    <!-- Proposals -->
    <b-field label="Proposals">
      <Proposals
        v-model="proposals" />
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';
import RolesAndUsers from '@/components/RolesAndUsers.vue';
import Proposals from '@/components/Proposals.vue';
import moment from 'moment';
import _ from 'lodash';

export default {
  components: { RolesAndUsers, Proposals },
  mixins: [
    CrudEditComponentMixin({
      properties: ['title', 'proposals', 'agenda']
    })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    const currentTime = new Date();
    const utcOffset = -(new Date().getTimezoneOffset());
    const startTime = this.entity.start
      ? moment.utc(this.entity.start).utcOffset(utcOffset, true).toDate()
      : currentTime;
    const endTime = this.entity.end
      ? moment.utc(this.entity.end).utcOffset(utcOffset, true).toDate()
      : currentTime;

    return {
      permissionsJoin: this.getPermissions('meeting.join'),
      permissionsVote: this.getPermissions('meeting.vote'),
      date: startTime,
      startTime,
      endTime
    };
  },
  computed: {
    permissionsDatabaseView() {
      return _
        .chain([])
        .concat(
          this.permissionsJoin
            .map(x => _.assign(x, { scope: 'meeting.join' })),
          this.permissionsVote
            .map(x => _.assign(x, { scope: 'meeting.vote' }))
        )
        .map(i => ({
          scope: i.scope,
          [i.type]: i._id
        }))
        .value();
    }
  },
  methods: {
    /**
     * Returns list of users or roles permitted to
     * participate in meeting keyed by permission type
     */
    getPermissions(scope) {
      const { roles, users } = this.$store.getters['names/get'];

      return _
        .chain(this.entity.permissions || [])
        .filter(p => p.scope === scope)
        .map(p => ({
          _id: p.role || p.user,
          name: p.role ? roles[p.role] : users[p.user],
          type: p.role ? 'role' : 'user',
          scope: p.scope
        }))
        .value();
    },

    test() {
      if (this.entity._id === undefined) {
        Object.assign(this.entity, { permissions: this.permissionsDatabaseView });
        return; // creating new entity. it is not in store yet
      }
      this.$store.dispatch('dashboard/meetings/update', {
        _id: this.entity._id, ...{ permissions: this.permissionsDatabaseView }
      });
    },

    timeChanged() {
      if (this.date && this.startTime && this.endTime) {
        const start = moment(this.date)
          .startOf('day')
          .add(this.startTime.getHours(), 'hours')
          .add(this.startTime.getMinutes(), 'minutes')
          .utcOffset(-0, true)
          .toISOString();
        const end = moment(this.date)
          .startOf('day')
          .add(this.endTime.getHours(), 'hours')
          .add(this.endTime.getMinutes(), 'minutes')
          .utcOffset(-0, true)
          .toISOString();

        this.update({
          start, end
        });
      }
    }
  },
  async fetch({
    store, entity, mass, newEntity
  }) {
    await Promise.all([
      store.dispatch('names/fetch', { collection: 'roles', field: 'name' }),
      store.dispatch('names/fetch', { collection: 'users', field: 'name' })
    ]);

    if (newEntity) { return; }

    // fetch related resources:
    // - parent zone
    // - assigned officials
    await mass.fetch(store, [
      { resource: 'proposals', list: entity.proposals }
    ]);
  }
};
</script>
