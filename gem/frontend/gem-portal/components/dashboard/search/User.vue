<template>
  <div>
    <nuxt-link
      :to="url">
      {{ entity.name }}
    </nuxt-link>
    <span
      v-for="role in entity.roles"
      :key="role._id"
      class="tag">
      {{ role.name }}
    </span>
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
      return `/dashboard/users/${this.entity._id}`;
    }
  }
};
</script>
