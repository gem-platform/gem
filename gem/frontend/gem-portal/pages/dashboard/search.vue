<template>
  <div>
    <!-- Search box -->
    <div class="box">
      <form @submit.prevent="submit">
        <b-input
          v-model="query"
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
      Nothong found
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
      nothingFound: false
    };
  },
  methods: {
    async submit() {
      // query db
      this.ready = {};

      const res = await this.$axios.$get(`${SEARCH_API}${this.query}`);
      this.results = _.groupBy(res, 'type');
      this.nothingFound = res.length === 0;

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
