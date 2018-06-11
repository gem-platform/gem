<template>
  <div>
    <!-- Search proposal field -->
    <div class="field">
      <b-autocomplete
        v-model="query"
        :data="searchResults"
        field="title"
        placeholder="Search proposal by title or index"
        icon="fas fa-search"
        @select="onSelected">
        <template slot="empty">No results found</template>
      </b-autocomplete>
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

            <!-- Move proposal up button -->
            <transition name="sort-button">
              <span
                v-if="index > 0"
                class="icon">
                <i
                  class="fa fa-angle-up"
                  @click="moveUp(index)"/>
              </span>
            </transition>

            <!-- Move proposal down button -->
            <transition name="sort-button">
              <span
                v-if="index+1 < list.length"
                class="icon">
                <i
                  class="fa fa-angle-down"
                  @click="moveDown(index)"/>
              </span>
            </transition>

            <!-- Remove proposal from list button -->
            <transition name="sort-button">
              <span class="icon">
                <i
                  class="fa fa-trash"
                  @click="remove(index)"/>
              </span>
            </transition>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import str from '@/lib/string';
import arr from '@/lib/array';

export default {
  props: {
    // Array of proposals to search in
    proposals: {
      type: Array,
      required: true
    },
    // Array of selected proposal IDs
    selected: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  data() {
    return {
      query: '', // Search query
      list: [] // Array of selected proposals (object)
    };
  },
  computed: {
    searchResults() {
      return this.proposals.filter(p =>
        str.contains(p.title, this.query) ||
        str.contains(p.index, this.query));
    }
  },
  watch: {
    list() {
      this.$emit('change', this.list.map(p => p._id));
    }
  },
  created() {
    // Convert list of selected ids to list of proposals (keeping order)
    this.list = this.selected.map(id => this.proposals.find(p => p._id === id));
  },
  methods: {
    moveUp(index) {
      arr.move(this.list, index, index - 1);
    },
    moveDown(index) {
      arr.move(this.list, index, index + 1);
    },
    remove(index) {
      arr.removeIndex(this.list, index);
    },
    onSelected(data) {
      // Selected proposal already been added
      const selectedIds = this.list.map(x => x._id);
      if (data === null) { return; }
      if (selectedIds.includes(data._id)) { return; }

      // Add selected proposal
      this.list.push(data);
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

.sort-button-enter-active, .sort-button-leave-active {
  transition: opacity .5s;
}
.sort-button-enter, .sort-button-leave-to {
  opacity: 0;
}
</style>
