<template>
  <b-autocomplete
    v-model="query"
    :loading="loading"
    :data="suggestions"
    :placeholder="placeholder"
    :field="field"
    :icon="icon"
    expanded
    @input="input"
    @select="selected">
    <template slot="empty">No results found</template>
    <template
      slot-scope="{option}"
      :slot="defaultSlotName">
      <slot :option="option"/>
    </template>
  </b-autocomplete>

</template>

<script>
import NotificationMixin from '@/components/NotificationMixin';
import regex from '@/lib/regex';

export default {
  mixins: [NotificationMixin],
  props: {
    value: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: 'fas fa-search'
    },
    placeholder: {
      type: String,
      default: 'Type to search'
    },
    field: {
      type: String,
      required: true
    },
    collection: {
      type: String,
      required: true
    },
    fields: {
      type: Array,
      required: false,
      default() { return []; }
    }
  },
  data() {
    return {
      query: this.value, // Search query,
      suggestions: [],
      loading: false
    };
  },
  computed: {
    defaultSlotName() {
      return this.$scopedSlots.default ? 'default' : 'not_default';
    }
  },
  methods: {
    /**
     * On input
     */
    async input(value) {
      this.$emit('input', value);

      // Field is empty, so emit nothing selected event
      if (value === '') {
        this.$emit('select', undefined);
      }

      // Input too short, abort
      if (!value || value.length < 1) {
        return;
      }

      // Fetch data
      try {
        this.loading = true;
        const result = await this.$axios.$get('/api/autocomplete', {
          params: {
            collection: this.collection,
            field: this.field,
            value: regex.escape(value),
            fields: this.fields
          }
        });
        this.suggestions = result.suggestions;
      } catch (e) {
        this.notify(e.response.data.message || e.message || 'Error', 'is-danger');
      } finally {
        this.loading = false;
      }
    },

    /**
     * On item selected
     */
    selected(data) {
      this.$emit('select', data);
    }
  }
};
</script>
