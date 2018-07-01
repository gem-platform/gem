<template>
  <a
    :download="downloadName"
    :href="downloadUrl"
    :class="{'is-loading': busy, 'is-success': downloadUrl}"
    class="button is-fullwidth"
    @click="click">
    <span class="icon">
      <span class="fa fa-print"/>
    </span>

    <span>
      {{ buttonTitle }}
    </span>
  </a>
</template>

<script>
import NotificationMixin from '@/components/NotificationMixin';

export default {
  mixins: [NotificationMixin],
  props: {
    title: {
      type: String,
      required: true
    },
    url: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      busy: false,
      downloadUrl: undefined,
      downloadName: undefined
    };
  },
  computed: {
    buttonTitle() {
      return this.downloadUrl ? `Download ${this.title}` : this.title;
    }
  },
  methods: {
    async click() {
      if (this.downloadUrl) {
        return;
      }

      this.busy = !this.busy;
      try {
        // const res =
        await this.$axios.$get(this.url, {});

        this.name = 'report.pdf';
        this.downloadUrl = '2.mp3';
        this.downloadName = 'report.pdf';
        this.busy = false;
      } catch (err) {
        this.notify('Report is not generated', 'is-danger');
      }
    }
  }
};
</script>

<style>
.button {
  transition: background-color 1.0s ease;
}
</style>
