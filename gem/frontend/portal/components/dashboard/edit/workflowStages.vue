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
    <div class="columns">
      <div class="column">
        <b-field
          label="Actions">
          <draggable
            v-model="actions"
            :options="{group: 'actions'}"
            class="drag-area">
            <div
              v-for="(action, index) in actions"
              :key="index"
              class="card action">

              <header class="card-header">
                <p class="card-header-title">
                  {{ action.id | name }}
                </p>
              </header>
              <div
                v-if="control(action.id)"
                class="card-content">
                <div
                  class="content">
                  <div :is="control(action.id)"/>
                </div>
              </div>

            </div>

            <div
              v-if="actions.length == 0">
              Drag some actions from the "Available actions" list.
            </div>
          </draggable>
        </b-field>
      </div>

      <!-- Available Actions -->
      <div class="column">
        <b-field
          label="Available actions">
          <draggable
            v-model="availableActions"
            :options="{sort: false, group: 'actions'}">
            <div
              v-for="action in availableActions"
              :key="action.id"
              class="card action">

              <header class="card-header">
                <p class="card-header-title">
                  {{ action.id | name }}
                </p>
              </header>
            </div>
          </draggable>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

import AcquaintanceActionConfig from '@/components/dashboard/edit/actions/AcquaintanceActionConfig.vue';

export default {
  filters: {
    name(id) {
      const map = {
        acquaintance: 'Acquaintance',
        discussion: 'Discussion',
        comments: 'Comments',
        ballot: 'Ballot',
        'ballot.results': 'Ballot Results'
      };
      return map[id];
    }
  },
  components: {
    draggable,
    AcquaintanceActionConfig
  },
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
    availableActions: {
      get() {
        return [
          { id: 'acquaintance' },
          { id: 'discussion' },
          { id: 'comments' },
          { id: 'ballot' },
          { id: 'ballot.results' }
        ];
      },
      set() { /* keep liist unmodified */ }
    }
  },
  methods: {
    control(id) {
      if (id === 'acquaintance') return AcquaintanceActionConfig;
      return undefined;
    }
  }
};
</script>

<style scoped>
.drag-area {
  min-height: 125px;
}

.action {
  margin-bottom: 15px;
}
</style>
