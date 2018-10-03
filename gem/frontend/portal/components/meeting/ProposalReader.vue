<template>
  <div>
    {{ mode }}
    <div
      ref="proposalContent"
      :class="{'in-parts-reader': mode=='in-parts'}"
      v-html="proposal.content"/>
    <br>

    <a
      v-if="mode == 'in-parts'"
      :class="moreButtonClass()"
      class="button is-fullwidth"
      @click="more">
      {{ moreButtonTitle() }}
    </a>
  </div>
</template>

<script>
import CommunicationMixin from '@/components/CommunicationMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  mixins: [StageStateMixin, CommunicationMixin],
  props: {
    mode: {
      type: String,
      default() { return 'all'; }
    }
  },
  data() {
    return { reveal: 10 };
  },
  computed: {
    /**
     * Proposal for current stage
     */
    proposal() {
      return this.stageProposal;
    }
  },
  methods: {
    /**
     * Reveal more content
     */
    more() {
      this.reveal += 150;
      this.$refs.proposalContent.style.maxHeight = `${this.reveal}px`;

      const percents = this.percents();
      if (percents) {
        this.send('reading_progress', { quantity: percents / 100 });
      }
    },

    /**
     * Get title of the button
     */
    moreButtonTitle() {
      const value = this.percents();
      if (value < 100) { return `Read more (${value}% done)`; }
      if (value >= 100) { return 'I read'; }
      return 'Read More';
    },

    moreButtonClass() {
      const value = this.percents();
      if (value >= 100) { return 'is-success'; }
      return 'is-light';
    },

    percents() {
      if (!this.$refs.proposalContent) { return undefined; }
      if (!this.$refs.proposalContent.scrollHeight) { return undefined; }

      const max = this.$refs.proposalContent.scrollHeight;
      const current = Math.min(this.reveal, max);
      const percents = Math.floor((current / max) * 100);

      return percents;
    }
  }
};
</script>

<style scoped>
.in-parts-reader {
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 100px;
  transition: all .5s;
}
</style>
