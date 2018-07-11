<template>
  <div>
    <b-message
      v-if="partially.yes"
      title="The data is partially displayed"
      type="is-warning">
      Only last {{ partially.count }} meetings are displayed
    </b-message>

    <b-message
      v-if="empty"
      type="is-warning">
      No scheduled meetings
    </b-message>

    <div
      v-for="(events, date) in schedule"
      :key="date">

      <!-- Date header -->
      <div class="notification is-primary has-text-centered">
        <p class="title">{{ date }}</p>
      </div>

      <!-- Events for current date -->
      <div
        v-for="event in events"
        :key="event._id">

        <!-- Event box -->
        <div
          :class="{'is-active': event.active}"
          class="schedule-time notification meeting-box">
          <div class="columns">
            <div class="column">
              <p :class="{'title': event.type == 'meeting'}">
                {{ event.title }}
              </p>
            </div>
            <div class="column has-text-right">
              <span class="tag is-medium">
                {{ event.start|time }} - {{ event.end|time }}
              </span>
            </div>
          </div>

          <!-- Event agenda -->
          <p v-if="event.agenda">
            {{ event.agenda }}
          </p>

          <!-- List of proposals -->
          <div
            v-if="event.proposals.length > 0"
            class="proposals-list">
            <p
              v-for="proposal in event.proposals"
              :key="proposal._id">
              <span class="icon">
                <i class="fa fa-angle-right"/>
              </span>
              <nuxt-link :to="proposal.url">{{ proposal.title }}</nuxt-link>
            </p>
            <br>
          </div>

          <!-- Join Button -->
          <transition name="fade">
            <div
              v-if="event.active || canManage"
              class="buttons is-centered">
              <nuxt-link
                :to="'/meeting/'+event._id"
                :class="{'is-primary': !canManage || event.active}"
                class="button is-fullwidth">
                {{ joinButtonTitle(event) }}
              </nuxt-link>
            </div>
          </transition>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import * as moment from 'moment';
import _ from 'lodash';

export default {
  filters: {
    time(value) {
      return moment.utc(value).format('HH:mm');
    }
  },
  mixins: [AuthMixin],
  layout: 'portal',
  computed: {
    /**
     * Get list of events to display
     */
    schedule() {
      // Subtract one hour in case meeting is little late
      const today = moment.utc().subtract(1, 'h');
      const allEvents = this.$store.getters['dashboard/meetings/list'];

      const schedule = allEvents.map(m => _.assign({}, m, {
        active: this.activeMeetings.includes(m._id),
        date: moment.utc(m.start).format('dddd, D MMMM'),
        type: (m.proposals) ? 'meeting' : 'break',
        proposals: (m.proposals || []).map(id => ({
          _id: id,
          title: this.proposalTitle(id),
          url: `/dashboard/proposals/${id}`
        }))
      }));

      return _
        .chain(schedule)
        .filter(m => (moment.utc(m.end) >= today))
        .sortBy('start')
        .groupBy('date')
        .value();
    },

    /**
     * There is no any scheduled meeting.
     */
    empty() {
      return Object.keys(this.schedule).length <= 0;
    },

    /**
     * Return list of active meetings
     */
    activeMeetings() {
      return this.$store.getters['meeting/status/active'];
    },

    /**
     * Is data displayed partially?
     */
    partially() {
      const meta = this.$store.getters['dashboard/meetings/meta'];
      return { yes: meta.total > meta.perPage, count: meta.perPage };
    },

    /**
     * Can user manage meeting?
     */
    canManage() {
      return this.haveAccess('meeting.manage');
    }
  },
  mounted() {
    this.$socket.on('meetings_status', this.onMeetingStatus);

    this.$socket.emit('meetings_status', (res) => {
      this.onMeetingStatus(res);
    });
  },
  beforeDestroy() {
    this.$socket.off('meetings_status', this.onMeetingStatus);
  },
  methods: {
    /**
     * Join button title
     */
    joinButtonTitle(event) {
      return this.canManage && !event.active ? 'Start' : 'Join';
    },

    /**
     * On meeting status data received
     */
    onMeetingStatus(data) {
      this.$store.dispatch('meeting/status/set', data);
    },

    /**
     * Get proposal title using specified ID
     */
    proposalTitle(id) {
      const proposals = this.$store.getters['dashboard/proposals/keyed'];
      return proposals[id] ? proposals[id].title : "<Proposal doesn't exist>";
    }
  }
};
</script>

<style scoped>
.schedule-time {
  margin-bottom: 1em;
  padding: 1em;
}
.proposals-list {
  padding-top: 1em;
}

.is-active {
  background-color: hsl(48, 100%, 67%);
}

.meeting-box {
  transition: background-color .5s ease;
}
</style>
