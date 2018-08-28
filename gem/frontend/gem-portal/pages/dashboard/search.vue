<template>
  <div>
    <!-- Search box -->
    <div class="box">
      <form @submit.prevent="submit">
        <b-input
          v-model="query"
          :loading="loading"
          placeholder="Search..."
          type="search"
          icon="fas fa-search"
          size="is-large"/>
      </form>
    </div>

    <!-- Search results -->
    <div
      v-for="(items, group) in results"
      v-if="ready[group] === true"
      :key="group"
      class="box content">

      <p class="heading">{{ group }}</p>
      <div
        v-for="(item, idx) in items"
        :key="idx">
        <div
          :is="item.type"
          :entity="entity(group, item._id)"/>
      </div>
    </div>

    <b-message
      v-show="nothingFound"
      type="is-danger">
      Nothing found
    </b-message>
  </div>
</template>

<script>
import _ from 'lodash';
import Comments from '@/components/dashboard/search/Comment.vue';
import Laws from '@/components/dashboard/search/Law.vue';
import Meetings from '@/components/dashboard/search/Meeting.vue';
import Officials from '@/components/dashboard/search/Official.vue';
import Proposals from '@/components/dashboard/search/Proposal.vue';
import Roles from '@/components/dashboard/search/Role.vue';
import Users from '@/components/dashboard/search/User.vue';
import Zones from '@/components/dashboard/search/Zone.vue';

const SEARCH_API = '/api/search?query=';

export default {
  layout: 'dashboard',
  components: {
    Comments, Laws, Meetings, Officials, Proposals, Roles, Users, Zones
  },
  data() {
    return {
      query: '',
      results: [],
      ready: {},
      nothingFound: false,
      loading: false,
      pendingRequestsCnt: 0
    };
  },
  watch: {
    pendingRequestsCnt(value) {
      this.loading = value !== 0;
    }
  },
  methods: {
    async submit() {
      this.ready = {};
      this.pendingRequestsCnt = 1;

      const res = await this.$axios.$get(`${SEARCH_API}${this.query}`);
      this.results = _.groupBy(res, 'type');
      this.nothingFound = res.length === 0;
      this.pendingRequestsCnt = Object.keys(this.results).length;

      Object.keys(this.results).forEach((entityType) => {
        this.$store.dispatch(
          `dashboard/${entityType}/fetchList`,
          {
            ids: this.results[entityType].map(x => x._id),
            params: { embedded: { roles: 1, cachedOfficials: 1, cachedZones: 1 } }
          }
        )
          .then(() => {
            this.$set(this.ready, entityType, true);
            this.pendingRequestsCnt -= 1;
          });
      });
    },
    entity(type, id) {
      const entity = this.$store.getters[`dashboard/${type}/keyed`];
      if (entity && entity[id]) {
        return { ...entity[id], ready: true, type };
      }
      return { _id: id, ready: false };
    }
  }
};
</script>
