<template>
  <div>
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
          :class="{'is-active': isActive(event._id)}"
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
              v-if="isActive(event._id)"
              class="buttons is-centered">
              <nuxt-link
                :to="'/meeting/'+event._id"
                class="button is-primary is-fullwidth">
                Join
              </nuxt-link>
            </div>
          </transition>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as moment from 'moment';
import _ from 'lodash';

export default {
  layout: 'portal',
  filters: {
    time(value) {
      return moment.utc(value).format('HH:mm');
    }
  },
  computed: {
    schedule() {
      const today = moment.utc();

      const meetings = this.$store.getters['dashboard/meetings/all'].map(m => ({
        _id: m._id,
        title: m.title,
        date: moment.utc(m.start).format('YYYY/MM/DD'),
        start: m.start,
        end: m.end,
        agenda: m.agenda,
        type: (m.agenda || m.proposals) ? 'meeting' : 'break',
        proposals: (m.proposals || []).map(id => ({
          _id: id,
          title: this.$store.getters['dashboard/proposals/get'](id)[0].title,
          url: `/dashboard/proposals/${id}`
        }))
      })).filter(m => (moment.utc(m.start) >= today));

      return _.chain(meetings).sortBy(['start']).groupBy('date').value();
    }
  },
  mounted() {
    this.$socket.emit('meetings_status', (res) => {
      this.$store.dispatch('meeting/status/set', res);
    });
  },
  methods: {
    isActive(meetingId) {
      const active = this.$store.getters['meeting/status/active'];
      return active.includes(meetingId);
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
  transition: background-color 1.5s ease;
}
</style>
