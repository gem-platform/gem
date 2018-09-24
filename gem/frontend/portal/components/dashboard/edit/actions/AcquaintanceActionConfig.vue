<template>
  <div>
    <b-switch
      v-model="parts">
      Show proposal in parts
    </b-switch>
  </div>
</template>

<script>
export default {
  data() {
    return {
      parts: false
    };
  }
};
</script>
