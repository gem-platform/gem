<template>
  <div>
    <!-- Index of proposal -->
    <b-field
      id="index-field"
      :type="validationHasError($v.index)"
      :message="validationMessages($v.index)"
      label="Index">
      <b-input
        id="index"
        v-model.trim="index"
        placeholder="Index"
        size="is-large" />
    </b-field>

    <!-- Title of proposal -->
    <b-field
      id="title-field"
      :type="validationHasError($v.title)"
      :message="validationMessages($v.title)"
      label="Title">
      <b-input
        id="title"
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
        id="workflow"
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
        id="stage"
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
        id="content"
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
      properties: [
        'index', 'title', 'content',
        { name: 'workflow', collection: 'workflowTypes' },
        { name: 'stage', collection: 'workflowStages' }
      ]
    })
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
    workflow: {
      required
    },
    stage: {
      required,
      belongToStage: (value, vm) => {
        if (vm.workflow && vm.workflow.stages) {
          return vm.workflow.stages.includes(value ? value._id : undefined);
        }
        return true;
      }
    },
    content: {
      required
    }
  },
  async fetch({
    store, entity, mass, newEntity
  }) {
    if (newEntity) { return; }

    // fetch related resources:
    // - selected workflow of the proposal
    // - selected stage of the proposal
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
