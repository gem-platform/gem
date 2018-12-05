<template>
  <BallotResults
    :header="null"/>
</template>

<script>
import BallotResults from '@/components/meeting/stages/widgets/BallotResults.vue';

export default {
  name: 'BallotResultsStageView',
  components: { BallotResults }
};
</script>
