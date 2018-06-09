<template>
  <div>
    <!-- Index of proposal -->
    <b-field
      :type="validationHasError($v.model.index)"
      :message="validationMessages($v.model.index)"
      label="Index">
      <b-input
        v-model.trim="model.index"
        placeholder="Index"
        size="is-large"
        @input="validationTouch($v.model.index)"/>
    </b-field>

    <!-- Title of proposal -->
    <b-field
      :type="validationHasError($v.model.title)"
      :message="validationMessages($v.model.title)"
      label="Title">
      <b-input
        v-model.trim="model.title"
        placeholder="Title"
        size="is-large"
        @input="validationTouch($v.model.title)"/>
    </b-field>

    <!-- Content of proposal -->
    <b-field
      :type="validationHasError($v.model.content)"
      :message="validationMessages($v.model.content)"
      label="Content">
      <div
        v-quill:myQuillEditor="editorOption"
        :content="model.content"
        class="quill-editor"
        @change="onEditorChange($event)"/>
    </b-field>

  </div>
</template>

<script>
import { required, alphaNum } from 'vuelidate/lib/validators';
import ValidationMixin from '@/components/ValidationMixin';

export default {
  mixins: [ValidationMixin],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      model: {
        index: this.entity.index,
        title: this.entity.title,
        content: this.entity.content || ''
      },
      editorOption: {
        modules: {
          toolbar: [
            [{ list: 'ordered' }, { list: 'bullet' }],
            ['bold', 'italic', 'underline', 'strike'],
            ['blockquote'],
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ align: [] }],
            ['clean']
          ]
        }
      }
    };
  },
  validations: {
    model: {
      index: { required, alphaNum },
      title: { required },
      content: { required }
    }
  },
  watch: {
    model: {
      handler() {
        Object.assign(this.entity, this.model);
      },
      deep: true
    }
  },
  methods: {
    onEditorChange({ editor, html, text }) {
      console.log('editor change!', editor, html, text);
      this.model.content = html;
    }
  }
};
</script>

<style scoped>
.quill-editor {
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
}
</style>
