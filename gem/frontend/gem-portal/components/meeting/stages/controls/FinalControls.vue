<template>
  <div
    class="field">
    <a
      v-if="showCloseButton"
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
      const res = await this.send('close', { });
      if (res.success) {
        this.notify('Meeting is closed');
      }
    }
  }
};
</script>
