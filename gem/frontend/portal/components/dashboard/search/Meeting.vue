<template>
  <div>
    <span class="tag time">{{ date }}</span>

    <nuxt-link
      :to="url">
      {{ entity.title }}
    </nuxt-link>

    <small v-if="entity.agenda">
      <br>
      {{ entity.agenda | truncate(256) }}
    </small>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    url() {
      return `/dashboard/meetings/${this.entity._id}`;
    },
    date() {
      return moment.utc(this.entity.start).fromNow();
      // .format('YYYY/MM/DD HH:mm');
    }
  }
};
</script>

<style scoped>
.time {
  font-feature-settings: "tnum";
}
</style>
