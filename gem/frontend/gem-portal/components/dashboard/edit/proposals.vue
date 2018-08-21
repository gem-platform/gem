<template>
  <div>
    <!-- Index of proposal -->
    <b-field
      :type="validationHasError($v.index)"
      :message="validationMessages($v.index)"
      label="Index">
      <b-input
        v-model.trim="index"
        placeholder="Index"
        size="is-large" />
    </b-field>

    <!-- Title of proposal -->
    <b-field
      :type="validationHasError($v.title)"
      :message="validationMessages($v.title)"
      label="Title">
      <b-input
        v-model.trim="title"
        placeholder="Title"
        size="is-large" />
    </b-field>

    <!-- Workflow of proposal -->
    <b-field
      :type="validationHasError($v.workflow)"
      :message="validationMessages($v.workflow)"
      label="Workflow">
      <Autocomplete
        :value="workflow ? workflow.name : ''"
        :fields="['_id']"
        field="name"
        collection="workflowTypes"
        placeholder="Type to search"
        @select="workflow = $event"/>
    </b-field>

    <!-- Stage of proposal -->
    <b-field
      :type="validationHasError($v.stage)"
      :message="validationMessages($v.stage)"
      label="Stage">
      <Autocomplete
        :value="stage ? stage.name : ''"
        :fields="['_id']"
        field="name"
        collection="workflowStages"
        placeholder="Type to search"
        @select="stage = $event"/>
    </b-field>

    <!-- Content of proposal -->
    <b-field
      :type="validationHasError($v.content)"
      :message="validationMessages($v.content)"
      label="Content">
      <div
        v-quill:editor="editorOption"
        :content="content"
        class="quill-editor"
        @change="content = $event.html"/>
    </b-field>

  </div>
</template>

<script>
// Mixins
import ValidationMixin from '@/components/ValidationMixin';
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';
import StoreMixin from '@/components/StoreMixin';

// Components
import Autocomplete from '@/components/Autocomplete.vue';

// Misc
import { required, minLength } from 'vuelidate/lib/validators';
import eoptions from '@/lib/config/editor';

export default {
  components: {
    Autocomplete
  },
  mixins: [
    ValidationMixin,
    CrudEditComponentMixin({
      properties: ['index', 'title', 'content', 'workflow', 'stage']
    }),
    StoreMixin([
      { collection: 'workflowTypes', name: '$wtypes' },
      { collection: 'workflowStages', name: '$wstages' }
    ])
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      editorOption: eoptions
    };
  },
  validations: {
    index: {
      required,
      minLength: minLength(4)
    },
    title: {
      required,
      minLength: minLength(4)
    },
    stage: {
      required
    },
    content: {
      required
    },
    workflow: {
      required
    }
  },
  computed: {
    /**
     * Workflow
     */
    workflow: {
      get() {
        return this.$wtypes.get(this.entity.workflow);
      },
      async set(value) {
        if (value && value._id) { await this.$wtypes.fetch(value._id); }
        this.update({ workflow: value ? value._id : undefined });
        this.$v.workflow.$touch();
      }
    },

    /**
     * Stage of the workflow
     */
    stage: {
      get() {
        return this.$wstages.get(this.entity.stage);
      },
      async set(value) {
        if (value && value._id) { await this.$wstages.fetch(value._id); }
        this.update({ stage: value ? value._id : undefined });
        this.$v.stage.$touch();
      }
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
      { resource: 'workflowTypes', one: entity.workflow },
      { resource: 'workflowStages', one: entity.stage }
    ]);
  }
};
</script>

<style scoped>
.quill-editor {
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  font-size: 1rem;
}
</style>
