<template>
  <div>
    <!-- Name -->
    <b-field
      label="Name"
      expanded>
      <b-input
        v-model="entity.name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <!-- Parent -->
    <b-field label="Parent">
      <ZoneSelect
        @change="onParentZoneChanged" />
    </b-field>

    <!-- Officials -->
    <b-field label="Officials">
      <b-input
        placeholder="Officials" />
    </b-field>
  </div>
</template>

<script>
import ZoneSelect from '@/components/ZoneSelect.vue';

export default {
  components: { ZoneSelect },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  methods: {
    onParentZoneChanged(parent) {
      this.entity.parent = parent ? parent._id : undefined;
    }
  }
};
</script>
