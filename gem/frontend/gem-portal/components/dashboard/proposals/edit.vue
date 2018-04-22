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
        size="is-large"
        @input="validationTouch($v.index)"/>
    </b-field>

    <!-- Title of proposal -->
    <b-field
      :type="validationHasError($v.title)"
      :message="validationMessages($v.title)"
      label="Title">
      <b-input
        v-model="title"
        placeholder="Title"
        size="is-large"
        @input="validationTouch($v.title)"/>
    </b-field>

    <!-- Content of proposal -->
    <b-field
      :type="validationHasError($v.content)"
      :message="validationMessages($v.content)"
      label="Content">
      <b-input
        v-model="content"
        type="textarea"
        placeholder="Content"
        @input="validationTouch($v.content)"/>
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
      index: this.entity.index,
      title: this.entity.title,
      content: this.entity.content || ''
    };
  },
  validations: {
    index: { required, alphaNum },
    title: { required },
    content: { required }
  },
  methods: {
    updateModel() {
      this.entity.index = this.index;
      this.entity.title = this.title;
      this.entity.content = this.content;
    }
  }
};
</script>
