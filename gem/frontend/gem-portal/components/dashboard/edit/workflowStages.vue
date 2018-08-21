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

    <!-- Description -->
    <b-field
      label="Description">
      <textarea
        v-model="description"
        class="textarea"
        placeholder="Description"/>
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  mixins: [
    CrudEditComponentMixin({ properties: ['name', 'description'] })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  }
};
</script>
