<template>
  <div>
    <nuxt-link
      :to="url">
      {{ entity.title }}
    </nuxt-link>
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
      return `/dashboard/propoals/${this.entity._id}`;
    }
  }
};
</script>
