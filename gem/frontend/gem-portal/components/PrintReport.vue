<template>
  <a
    :download="downloadName"
    :href="downloadUrl"
    :class="{'is-loading': busy,
             'is-success': downloadUrl,
             'is-danger': error}"
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
    },
    filename: {
      type: String,
      default() { return undefined; }
    },
    params: {
      type: Object,
      default() { return {}; }
    }
  },
  data() {
    return {
      busy: false,
      downloadUrl: undefined,
      downloadName: undefined,
      error: undefined
    };
  },
  computed: {
    /**
     * Gets title for button
     */
    buttonTitle() {
      return this.downloadUrl
        ? `Download "${this.title}"`
        : this.error || this.title;
    }
  },
  methods: {
    async click() {
      // report already generated and
      // url to download it provided
      if (this.downloadUrl) {
        this.downloadUrl = undefined;
        return;
      }

      // generate report
      try {
        this.error = undefined;
        this.busy = true;
        const res = await this.$axios.$get(this.url, { params: this.params });

        this.downloadUrl = `/downloads/${res.filename}`;
        this.downloadName = this.filename || res.filename;
      } catch (err) {
        this.notify('Report is not generated', 'is-danger');
        this.error = err.message || 'Report is not generated';
      } finally {
        this.busy = false;
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
