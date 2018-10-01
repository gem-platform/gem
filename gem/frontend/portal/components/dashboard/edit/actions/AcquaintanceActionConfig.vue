<template>
  <div>
    <b-field label="Proposal display mode">
      <b-select
        v-model="proposalDisplayMode"
        placeholder="Proposal display mode"
        expanded
        @input="changed">
        <option value="full">Entirely</option>
        <option value="in-parts">In parts</option>
      </b-select>
    </b-field>


    <b-field label="Comments display mode">
      <b-select
        v-model="commentsDisplayMode"
        placeholder="Comments display mode"
        expanded
        @input="changed">
        <option value="all">All comments</option>
        <option value="prev-stage">From previous stage only</option>
      </b-select>
    </b-field>


    <b-field label="Ballot display mode">
      <b-select
        v-model="ballotDisplayMode"
        placeholder="Ballot display mode"
        expanded
        @input="changed">
        <!--<option value="all">All ballots</option>-->
        <option value="prev-stage">From previous stage only</option>
      </b-select>
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Object,
      default() { return {}; }
    }
  },
  data() {
    return {
      proposalDisplayMode: this.value.proposalDisplayMode || 'full',
      commentsDisplayMode: this.value.commentsDisplayMode || 'prev-stage',
      ballotDisplayMode: this.value.ballotDisplayMode || 'prev-stage'
    };
  },
  methods: {
    changed() {
      this.$emit('change', {
        proposalDisplayMode: this.proposalDisplayMode,
        commentsDisplayMode: this.commentsDisplayMode,
        ballotDisplayMode: this.ballotDisplayMode
      });
    }
  }
};
</script>
