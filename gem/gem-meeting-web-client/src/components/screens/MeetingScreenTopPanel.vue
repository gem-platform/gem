<template>
  <div>
    <section class="hero is-primary is-small">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{ title }}
          </h1>
          <h2 class="subtitle">
            {{ subtitle }}
          </h2>
        </div>
      </div>
    </section>
  </div>
</template>

<script>

export default {
  name: 'MeetingScreenTopPanel',
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: '',
    },
  },
};
</script>
