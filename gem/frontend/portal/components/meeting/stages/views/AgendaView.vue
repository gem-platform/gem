<template>
  <div>
    <!-- List of proposals to bew reviews -->
    <div>
      <p class="heading has-text-centered">
        Proposals
      </p>
      <div
        v-for="(proposal, index) in proposals"
        :key="index">
        <span class="icon">
          <i class="fa fa-file"/>
        </span>
        <span>{{ proposal.title }}</span>
      </div>
    </div>

    <!-- Agenda -->
    <div v-if="content">
      <p class="heading has-text-centered">
        Agenda
      </p>
      <div class="content">
        {{ content }}
      </div>
    </div>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  mixins: [StageStateMixin],
  computed: {
    /**
     * Returns agenda for current meeting
     */
    content() {
      const { content } = this.$store.getters['meeting/stage/state'];
      return content;
    }
  }
};
</script>
