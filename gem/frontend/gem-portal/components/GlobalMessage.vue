<template>
  <section class="notification">
    <div class="has-text-centered">
      <h1 class="title capitalize">
        {{ title }}
      </h1>
      <h2 class="subtitle">
        {{ message }}
      </h2>
    </div>
  </section>
</template>

<script>
export default {
  name: 'GlobalMessage',
  props: {
    title: {
      type: String,
      default: 'Error'
    },
    message: {
      type: String,
      default: 'Some error occurred'
    }
  }
};
</script>

<style scoped>
.capitalize {
  text-transform:capitalize;
}
</style>
