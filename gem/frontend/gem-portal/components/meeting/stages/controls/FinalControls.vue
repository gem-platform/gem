<template>
  <div
    class="field">
    <a
      v-if="showCloseButton || true"
      class="button control is-fullwidth is-danger"
      @click="close">
      <span class="icon is-small">
        <i class="fa fa-times"/>
      </span>
      <span>Close meeting</span>
    </a>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import CommunicationMixin from '@/components/CommunicationMixin';

export default {
  name: 'FinalStageControls',
  mixins: [AuthMixin, NotificationMixin, CommunicationMixin],
  computed: {
    showCloseButton() {
      return this.haveAccess('meeting.manage');
    }
  },
  methods: {
    /**
     * Close meeting
     */
    async close() {
      try {
        await this.send('close', { });
      } catch (err) {
        this.notify(err.message, 'is-danger');
      }
    }
  }
};
</script>
