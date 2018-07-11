<template>
  <div>
    <!-- Index of law -->
    <b-field
      label="Index">
      <b-input
        v-model.trim="index"
        placeholder="Index"
        size="is-large"/>
    </b-field>

    <!-- Title of law -->
    <b-field
      label="Title">
      <b-input
        v-model.trim="title"
        placeholder="Title"
        size="is-large"/>
    </b-field>

    <!-- Content of law -->
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
      editorOption: eoptions
    };
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
