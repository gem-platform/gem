<template>
  <div>
    <!-- Content of proposal -->
    <b-field
      label="Content">
      <textarea
        v-model="content"
        class="textarea"
        placeholder="Write your comment here"/>
    </b-field>

  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  mixins: [
    CrudEditComponentMixin({ properties: ['content'] })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  }
};
</script>
