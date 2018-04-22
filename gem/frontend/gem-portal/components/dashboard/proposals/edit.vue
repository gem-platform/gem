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
      <b-input
        v-model.trim="model.content"
        type="textarea"
        placeholder="Content"
        @input="validationTouch($v.model.content)"/>
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
  }
};
</script>
