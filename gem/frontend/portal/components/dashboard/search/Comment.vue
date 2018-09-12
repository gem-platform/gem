<template>
  <div>
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
