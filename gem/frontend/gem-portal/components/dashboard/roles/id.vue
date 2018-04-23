<template>
  <div>
    <h1>{{ entity.name }}</h1>
    {{ entity.permissions }}
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
