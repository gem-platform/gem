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
              {{ proposal.stage | stage }}
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
import Autocomplete from '@/components/Autocomplete.vue';
import arr from '@/lib/array';
import flow from '@/lib/flow';

export default {
  components: {
    Autocomplete
  },
  filters: {
    stage(value) {
      const stage = flow.stages.find(s => s.value === value);
      return stage ? stage.title : '';
    }
  },
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
      list: this.value.map(id => proposals[id])
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
      if (data === null) { return; }
      if (this.selectedIds.includes(data._id)) { return; }

      // Add selected proposal
      this.list.push(data);
      this.$emit('input', this.selectedIds);
      this.query = '';
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
