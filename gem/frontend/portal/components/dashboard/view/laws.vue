<template>
  <div>
    <h1>{{ entity.title }}</h1>
    <div v-html="entity.content"/>
  </div>
</template>

<script>
export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  }
};
</script>
