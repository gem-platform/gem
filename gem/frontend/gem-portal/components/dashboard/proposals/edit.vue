<template>
  <div>
    <b-field label="Index">
      <b-input
        v-model="entity.index"
        placeholder="Index"
        size="is-large"/>
    </b-field>

    <b-field label="Title">
      <b-input
        v-model="entity.title"
        placeholder="Title"
        size="is-large"/>
    </b-field>

    <b-field label="Content">
      <b-input
        v-model="entity.content"
        type="textarea"
        placeholder="Content"/>
    </b-field>
  </div>
</template>

<script>
export default {
  props: ['entity']
};
</script>
