<template>
  <div>
    <p class="title">
      Welcome back, {{ name }}!
    </p>

    <div class="columns">
      <div class="column is-8">
        <div
          v-for="(events, date) in schedule.events"
          :key="date">

          <div class="notification is-info">
            <nav class="level is-mobile">
              <div class="level-item has-text-centered">
                <div>
                  <p class="title">{{ date }}</p>
                </div>
              </div>
            </nav>

          </div>

          <div
            v-for="event in events"
            :key="event._id">

            <div class="schedule-time notification">
              <div class="columns">
                <div class="column">
                  <p :class="{'title': event.type == 'meeting'}">
                    {{ event.title }}
                  </p>
                </div>
                <div class="column has-text-right">
                  <p :class="{'subtitle': event.type == 'meeting'}">
                    {{ event.start|time }} - {{ event.end|time }}
                  </p>
                </div>
              </div>

              <p v-if="event.agenda">
                {{ event.agenda }}
              </p>

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
              </div>

            </div>
          </div>
        </div>
      </div>

      <div class="column is-4">
        <!-- keep -->
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
  data() {
    return ({
    });
  },
  computed: {
    name() {
      return this.$auth.user.name;
    },
    schedule() {
      const meetings = this.$store.getters['dashboard/meetings/all'].map(m => ({
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
      }));


      return {
        events: _.chain(meetings).sortBy(['start']).groupBy('date').value()
      };
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/meetings/fetch');
    await store.dispatch('dashboard/proposals/fetch');
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
</style>
