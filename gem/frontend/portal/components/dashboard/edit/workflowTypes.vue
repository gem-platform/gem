<template>
  <div>
    <!-- Name -->
    <b-field
      label="Name">
      <b-input
        v-model.trim="name"
        placeholder="Name"
        size="is-large" />
    </b-field>

    <!-- Stages -->
    <b-field label="Stages">
      <WorkflowStagesList
        v-model="stages" />
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';
import WorkflowStagesList from '@/components/WorkflowStagesList.vue';

export default {
  components: {
    WorkflowStagesList
  },
  mixins: [
    CrudEditComponentMixin({ properties: ['name', 'stages'] })
  ],
  props: {
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
      { resource: 'workflowStages', list: entity.stages }
    ]);
  }
};
</script>
