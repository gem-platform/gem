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
        v-model="parent" />
    </b-field>

    <!-- Officials -->
    <b-field label="Officials">
      <OfficialsList/>
    </b-field>
  </div>
</template>

<script>
import ZoneSelect from '@/components/ZoneSelect.vue';
import OfficialsList from '@/components/OfficialsList.vue';

export default {
  components: { ZoneSelect, OfficialsList },
  filters: {
    join(value) {
      return value.join(', ');
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      parent: this.entity.parent
    };
  },
  methods: {
    onParentZoneChanged(parent) {
      console.log(parent);
      this.entity.parent = parent ? parent._id : undefined;
    }
  }
};
</script>
