<template>
  <div>
    <nuxt-link
      :to="url">
      {{ entity.name }}
    </nuxt-link>

    <br>
    <div class="margin">
      <span
        v-if="entity.cachedZones"
        class="tags">
        <span
          v-for="zone in entity.cachedZones"
          :key="zone._id"
          class="tag">
          {{ zone.name }}
        </span>
      </span>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    url() {
      return `/dashboard/officials/${this.entity._id}`;
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
