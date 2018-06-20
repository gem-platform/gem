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
      :key="r.id"
      class="content">

      <!-- Law title -->
      <nuxt-link :to="r.url">
        <h2 v-html="r.title"/>
      </nuxt-link>

      <!-- Search highlights -->
      <ul>
        <li
          v-for="(h, id) in r.highlights"
          :key="id">
          <span v-html="h"/>
        </li>
      </ul>
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
      this.results = res.hits.hits.map(x => ({
        id: x._id,
        title: (x.highlight.title && x.highlight.title[0]) || x._source.title,
        highlights: x.highlight.content,
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
