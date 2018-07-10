<template>
  <div>
    <!-- Name -->
    <b-field
      label="Name"
      expanded>
      <b-input
        v-model="name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <!-- Parent -->
    <b-field label="Parent">
      <ZoneSelect
        v-model="parent" />
    </b-field>

    <!-- Officials list -->
    <b-field label="Officials">
      <OfficialsList
        v-model="officials" />
    </b-field>
  </div>
</template>

<script>
import ZoneSelect from '@/components/ZoneSelect.vue';
import OfficialsList from '@/components/OfficialsList.vue';
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  components: { ZoneSelect, OfficialsList },
  mixins: [
    /**
     * Provide properties to update entity
     */
    CrudEditComponentMixin({
      properties: ['name', 'parent', 'officials']
    })
  ],
  props: {
    /**
     * Entity to edit
     */
    entity: {
      type: Object,
      required: true
    }
  },
  async fetch({
    store, entity, mass, newEntity
  }) {
    if (newEntity) { return; }

    // fetch related resources:
    // - parent zone
    // - assigned officials
    await mass.fetch(store, [
      { resource: 'zones', one: entity.parent },
      { resource: 'officials', list: entity.officials }
    ]);
  }
};
</script>
