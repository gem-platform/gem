<template>
  <BallotResults
    :header="null"
    :show-result="showResult" />
</template>

<script>
import BallotResults from '@/components/meeting/stages/widgets/BallotResults.vue';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

export default {
  name: 'BallotResultsStageView',
  components: { BallotResults },
  mixins: [StageStateMixin],
  computed: {
    /**
     * Show pass/fail?
     */
    showResult() {
      const { config } = this.$stage;
      return config ? config.showResult : false;
    }
  }
};
</script>
