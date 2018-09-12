<template>
  <div>
    <nuxt-link
      :to="url">
      {{ entity.name }}
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
      return `/dashboard/role/${this.entity._id}`;
    }
  }
};
</script>
