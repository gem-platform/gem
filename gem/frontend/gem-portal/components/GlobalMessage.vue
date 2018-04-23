<template>
  <section class="box notification">
    <div class="has-text-centered">
      <h1 class="title">
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
