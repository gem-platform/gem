<template>
  <div>
    <div
      v-for="meeting in meetings"
      :key="meeting._id"
      :class="{'is-active': isActive(meeting._id)}"
      class="box notification meeting-box">

      <div class="level">
        <div class="level-left">
          <div class="level-item ">
            <div>
              <p class="heading">Title</p>
              <p class="title">
                {{ meeting.title }}
              </p>
            </div>
          </div>
        </div>

        <div
          v-if="isActive(meeting._id)"
          class="level-right">
          <div
            class="level-item has-text-centered">
            <div>
              <p class="heading">Online</p>
              <p class="title">
                {{ online(meeting._id) }}
              </p>
            </div>
          </div>
        </div>

        <div
          v-else
          class="level-right">
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Date</p>
              <p class="title">{{ meeting.start | date }}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Start</p>
              <p class="title">{{ meeting.start | time }}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">End</p>
              <p class="title">{{ meeting.end | time }}</p>
            </div>
          </div>
        </div>
      </div>

      <p>{{ meeting.agenda }}</p>

      <br>
      <div
        v-for="proposal in meeting.proposals"
        :key="proposal">

        <span class="icon">
          <i class="fa fa-file"/>
        </span>

        <nuxt-link
          :to="'/dashboard/proposals/'+proposal">{{ title(proposal) }}
        </nuxt-link>
      </div>

      <br>
      <div
        v-if="isActive(meeting._id)"
        class="buttons is-centered">
        <nuxt-link
          :to="'/meeting/'+meeting._id"
          class="button is-primary is-fullwidth">
          Join
        </nuxt-link>
      </div>

    </div>
  </div>
</template>

<script>
import * as moment from 'moment';
import time from '@/lib/time';

export default {
  layout: 'portal',
  filters: {
    date(value) {
      const date = time.parseIsoDatetime(value);
      return moment(date).calendar(null, {
        sameDay: '[Today]',
        nextDay: '[Tomorrow]',
        nextWeek: 'dddd',
        lastDay: '[Yesterday]',
        lastWeek: '[Last] dddd',
        sameElse: 'DD/MM/YYYY'
      });
    },
    time(value) {
      const date = time.parseIsoDatetime(value);
      return moment(date).format('HH:mm');
    }
  },
  computed: {
    meetings() {
      return this.$store.getters['dashboard/meetings/all'];
    }
  },
  mounted() {
    this.$socket.emit('status');
  },
  methods: {
    title(proposalId) {
      const proposal = this.$store.getters['dashboard/proposals/get'](proposalId)[0];
      return proposal ? proposal.title : 'No proposal found';
    },
    isActive(meetingId) {
      const active = this.$store.getters['meeting/status/active'];
      return active.includes(meetingId);
    },
    online(meetingId) {
      const online = this.$store.getters['meeting/status/online'];
      return online[meetingId] || 0;
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/meetings/fetch');
    await store.dispatch('dashboard/proposals/fetch');
  }
};
</script>

<style scoped>
.is-active {
  background-color: hsl(48, 100%, 67%);
}

.meeting-box {
  transition: background-color 1.5s ease;
}
</style>
