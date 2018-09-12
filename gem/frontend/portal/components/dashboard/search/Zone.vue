<template>
  <div class="control">
    <nuxt-link
      :to="url">
      {{ entity.name }}
    </nuxt-link>
    <br>

    <div class="margin">
      <small>{{ entity.path | join }}</small>
      <span class="tags">
        <span
          v-for="official in entity.cachedOfficials"
          :key="official._id"
          class="tag">
          {{ official.name }}
        </span>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  filters: {
    join(value) {
      if (!value) { return ''; }
      return value.join(' / ');
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    url() {
      return `/dashboard/zones/${this.entity._id}`;
    }
  }
};
</script>

<style scoped>
.margin {
  margin-left: 15px;
  margin-bottom: 10px;
}
</style>
