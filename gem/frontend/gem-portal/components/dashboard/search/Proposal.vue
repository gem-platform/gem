<template>
  <div>
    <nuxt-link
      :to="url">
      {{ entity.title }}
    </nuxt-link>

    <div class="tag">
      {{ entity.stage | stage }}
    </div>
  </div>
</template>

<script>
import flow from '@/lib/flow';

export default {
  filters: {
    stage(value) {
      const stage = flow.stages.find(s => s.value === value);
      return stage ? stage.title : '';
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
      return `/dashboard/propoals/${this.entity._id}`;
    }
  }
};
</script>
