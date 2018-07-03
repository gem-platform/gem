<template>
  <div>
    <b-autocomplete
      v-model="query"
      :loading="loading"
      :data="suggestions"
      :placeholder="placeholder"
      :field="field"
      icon="fas fa-search"
      @input="onInput"
      @select="onSelected">
      <template slot="empty">No results found</template>
      <template slot-scope="props">
        <slot :option="props.option"/>
      </template>
    </b-autocomplete>
  </div>
</template>

<script>
import NotificationMixin from '@/components/NotificationMixin';
import regex from '@/lib/regex';

export default {
  mixins: [NotificationMixin],
  props: {
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
      query: '', // Search query,
      suggestions: [],
      loading: false
    };
  },
  methods: {
    async onInput(value) {
      this.$emit('input', value);
      if (!value || value.length < 1) { return; }

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
    onSelected(data) {
      this.$emit('select', data);
    }
  }
};
</script>
