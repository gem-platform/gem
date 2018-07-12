<template>
  <div>
    <div class="columns">
      <div class="column is-8 is-offset-2">
        <p class="title">
          Welcome back, {{ name }}!
        </p>
        <Schedule/>
      </div>
    </div>
  </div>
</template>

<script>
import Schedule from '@/components/Schedule.vue';
import * as moment from 'moment';
import _ from 'lodash';

export default {
  layout: 'portal',
  components: { Schedule },
  computed: {
    name() {
      return this.$auth.user.name;
    }
  },
  async fetch({ store }) {
    const now = moment.utc().subtract(1, 'h');

    // Fetch list of meetings to be displayed at page
    const meetings = await store.dispatch('dashboard/meetings/fetchPage', {
      max_results: 50,
      where: {
        start: { $gte: now.toISOString() }
      }
    });

    // Fetch related proposals if required
    const proposalIds = _
      .chain(meetings._items)
      .map(m => m.proposals)
      .filter(ids => ids !== undefined)
      .flatten()
      .value();
    if (proposalIds && proposalIds.length > 0) {
      await store.dispatch('dashboard/proposals/fetchList', proposalIds);
    }
  }
};
</script>
