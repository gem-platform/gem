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

    <!-- Actions -->
    <label class="label">Actions</label>
    <div
      v-for="action in actionsList"
      :key="action.id">
      <b-checkbox
        v-model="actions"
        :native-value="action.id"
        class="field">
        {{ action.name }}
      </b-checkbox>
    </div>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  mixins: [
    CrudEditComponentMixin({
      properties: ['name', 'description', 'actions']
    })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    actionsList() {
      return [
        { id: 'acquaintance', name: 'Acquaintance' },
        { id: 'ballot', name: 'Ballot' },
        { id: 'ballot.results', name: 'Ballot Results' },
        { id: 'comments', name: 'Comments' },
        { id: 'discussion', name: 'Discussion' }
      ];
    }
  }
};
</script>
