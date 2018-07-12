<template>
  <div>
    <!-- Index of proposal -->
    <b-field
      label="Index">
      <b-input
        v-model.trim="index"
        placeholder="Index"
        size="is-large" />
    </b-field>

    <!-- Title of proposal -->
    <b-field
      label="Title">
      <b-input
        v-model.trim="title"
        placeholder="Title"
        size="is-large" />
    </b-field>

    <!-- Stage of proposal -->
    <b-field
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
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

import flow from '@/lib/flow';
import eoptions from '@/lib/config/editor';

export default {
  mixins: [
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
