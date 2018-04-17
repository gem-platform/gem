<template>
  <div>
    <h1>{{ entity.title }} ({{ entity.index }})</h1>
    {{ entity.content }}
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
