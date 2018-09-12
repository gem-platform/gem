<template>
  <div>
    <!-- Search proposal field -->
    <div class="field">
      <Autocomplete
        v-model="query"
        :fields="['_id', 'title', 'stage']"
        collection="proposals"
        field="title"
        @select="selected"/>
    </div>

    <!-- List of selected proposals -->
    <div>
      <transition-group
        name="proposals-list"
        tag="ul">
        <div
          v-for="(proposal, index) in list"
          :key="proposal._id"
          class="proposal-list-item level">

          <div class="level-left">
            <span class="icon">
              <i class="fa fa-file"/>
            </span>
            {{ proposal.title }}
          </div>

          <!-- Control buttons: up, down, delete -->
          <div class="level-right">
            <!-- Stage of proposal -->
            <span class="stage">
              {{ stageName(proposal.stage) }}
            </span>

            <!-- Move proposal up button -->
            <span
              class="icon">
              <i
                class="fa fa-angle-up"
                @click="up(index)"/>
            </span>

            <!-- Move proposal down button -->
            <span
              class="icon disabled">
              <i
                class="fa fa-angle-down"
                @click="down(index)"/>
            </span>

            <!-- Remove proposal from list button -->
            <span class="icon">
              <i
                class="fa fa-trash"
                @click="remove(index)"/>
            </span>

          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
// Mixins
import StoreMixin from '@/components/StoreMixin';

// Components
import Autocomplete from '@/components/Autocomplete.vue';

// Misc
import arr from '@/lib/array';

export default {
  components: {
    Autocomplete
  },
  mixins: [
    StoreMixin([
      { collection: 'workflowStages', name: 'wstages' }
    ])
  ],
  props: {
    // Array of selected proposal IDs
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    const proposals = this.$store.getters['dashboard/proposals/keyed'];

    return {
      query: '', // Search query
      list: this.value.map(id => proposals[id] || { _id: id, title: '<Removed>' })
    };
  },
  computed: {
    selectedIds() {
      return this.list.map(x => x._id);
    }
  },
  methods: {
    /**
     * Move proposal up
     */
    up(index) {
      arr.move(this.list, index, index - 1);
      this.$emit('input', this.selectedIds);
    },

    /**
     * Move proposal down
     */
    down(index) {
      arr.move(this.list, index, index + 1);
      this.$emit('input', this.selectedIds);
    },

    /**
     * Remove proposal
     */
    remove(index) {
      arr.removeIndex(this.list, index);
      this.$emit('input', this.selectedIds);
    },

    /**
     * On proposal selected
     */
    selected(data) {
      // Selected proposal already been added
      if (!data) { return; }
      if (this.selectedIds.includes(data._id)) { return; }

      // fetch some data
      this.wstages.fetch(data.stage);

      // Add selected proposal
      this.list.push(data);
      this.$emit('input', this.selectedIds);
      this.query = '';
    },

    /**
     * Get name of the stage
     */
    stageName(id) {
      const stage = this.wstages.get(id);
      if (!stage) { this.wstages.fetch(id); }
      return stage ? stage.name : '';
    }
  }
};
</script>

<style sccoped>
.proposal-list-item {
  margin-bottom: 0em !important;
}

.proposals-list-move {
  transition: transform .5s;
}

.proposals-list-enter-active, .proposals-list-leave-active {
  transition: all 1s;
}
.proposals-list-enter, .proposals-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.stage {
  margin-left: 1em;
  color: gray;
}
</style>
