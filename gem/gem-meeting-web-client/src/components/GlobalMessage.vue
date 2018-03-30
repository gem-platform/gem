<template>
  <section class="hero is-fullheight">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">
          {{ title }}
        </h1>
        <h2 class="subtitle">
          {{ message }}
        </h2>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'GlobalMessage',
  props: {
    title: {
      type: String,
      default: 'Error',
    },
    message: {
      type: String,
      default: 'Some error occurred',
    },
  },
};
</script>
