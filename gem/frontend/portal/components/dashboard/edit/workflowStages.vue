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
                class="card-content">
                <div
                  class="content">
                  <!-- basic config -->
                  <basic-action-config
                    :value="action.config"
                    @change="actionChanged({index, id: action.id, value: $event})"/>

                  <!-- specific config -->
                  <div
                    :is="control(action.id)"
                    :value="action.config"
                    @change="actionChanged({index, id: action.id, value: $event})"/>
                </div>
              </div>
            </div>

            <!-- No actions added yet -->
            <div
              v-if="actions.length == 0">
              No actions added yet. Drag some actions from the "Available actions" list here.
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
import Draggable from 'vuedraggable';
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

import BasicActionConfig from '@/components/dashboard/edit/actions/BasicActionConfig.vue';
import AcquaintanceActionConfig from '@/components/dashboard/edit/actions/AcquaintanceActionConfig.vue';
import BallotActionConfig from '@/components/dashboard/edit/actions/BallotActionConfig.vue';
import BallotResultsActionConfig from '@/components/dashboard/edit/actions/BallotResultsActionConfig.vue';

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
    Draggable,
    AcquaintanceActionConfig,
    BallotActionConfig,
    BallotResultsActionConfig,
    BasicActionConfig
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
      if (id === 'ballot') return BallotActionConfig;
      if (id === 'ballot.results') return BallotResultsActionConfig;
      return undefined;
    },
    actionChanged({ index, value }) {
      const entityId = this.$route.params.id;
      this.$store.commit('dashboard/workflowStages/setActionConfig', {
        id: entityId, index, value
      });
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
