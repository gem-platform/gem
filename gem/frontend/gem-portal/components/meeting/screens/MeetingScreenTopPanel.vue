<template>
  <div class="box notification is-light">
    <h1 class="title">
      {{ title }}
    </h1>
    <h2 class="subtitle">
      {{ subtitle }}
    </h2>
  </div>
</template>

<script>
export default {
  name: 'MeetingScreenTopPanel',
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    }
  }
};
</script>
