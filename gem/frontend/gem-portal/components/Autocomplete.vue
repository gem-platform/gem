<template>
  <div>
    <b-autocomplete
      v-model="query"
      :loading="loading"
      :data="suggestions"
      :placeholder="placeholder"
      :field="field"
      :icon="icon"
      @input="onInput"
      @select="onSelected">
      <template slot="empty">No results found</template>
      <template
        slot-scope="{option}"
        :slot="defaultSlotName">
        <slot :option="option"/>
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
      this.$emit('select', data ? data._id.$oid : undefined);
    }
  }
};
</script>
