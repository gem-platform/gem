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

    <!-- Stage of proposal -->
    <b-field
      :type="validationHasError($v.stage)"
      :message="validationMessages($v.stage)"
      label="Stage">
      <b-autocomplete
        v-model="stage"
        :data="stages"
        :keep-first="true"
        :open-on-focus="true"
        placeholder="Stage"
        field="title"/>
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
import ValidationMixin from '@/components/ValidationMixin';
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

import { required, minLength } from 'vuelidate/lib/validators';

import flow from '@/lib/flow';
import eoptions from '@/lib/config/editor';

export default {
  mixins: [
    ValidationMixin,
    CrudEditComponentMixin({ properties: ['index', 'title', 'content'] })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      stages: flow.stages,
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
    }
  },
  computed: {
    /**
     * Stage of proposal
     *
     * Converts value 'deputy:review' to Deputy review and vice versa.
     */
    stage: {
      get() {
        const stage = flow.stages.find(x => x.value === this.entity.stage);
        return stage ? stage.title : '';
      },
      set(stage) {
        const f = flow.stages.find(x => x.title === stage);
        if (f) { this.update({ stage: f.value }); }
        this.$v.stage.$touch();
      }
    }
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
