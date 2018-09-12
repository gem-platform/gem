<template>
  <div>
    <!-- Search box -->
    <div class="box">
      <form @submit.prevent="submit">
        <b-input
          v-model="query"
          placeholder="Search..."
          type="search"
          icon="fas fa-search"/>
      </form>
    </div>

    <!-- Search results -->
    <div
      v-for="r in results"
      :key="r._id"
      class="notification is-grey content">

      <!-- Law title -->
      <nuxt-link :to="r.url">
        <h2 v-html="r.title"/>
      </nuxt-link>

      <!-- Search highlights -->
      <span v-html="r.highlights"/>
    </div>
  </div>
</template>

<script>
const SEARCH_API = '/api/laws/search?query=';

export default {
  layout: 'portal',
  data() {
    return {
      query: '',
      results: []
    };
  },
  methods: {
    async submit() {
      // query db
      const res = await this.$axios.$get(`${SEARCH_API}${this.query}`);

      // map search results
      this.results = res.map(x => ({
        _id: x._id,
        title: x.title,
        highlights: x.highlights,
        url: `/dashboard/laws/${x._id}`
      }));
    }
  }
};
</script>

<style>
em {
  font-style: bold;
  background-color: yellow;
}
</style>
