<template>
  <div>
    <b-autocomplete
      v-model="query"
      :loading="loading"
      :data="suggestions"
      field="name"
      placeholder="Search zone by name"
      icon="fas fa-search"
      @input="onInput"
      @select="onSelected">
      <template slot="empty">No results found</template>
      <template slot-scope="props">
        <div class="media">
          <div class="media-content">
            <span v-html="highlight(props.option.name)"/>
            <br>
            <small v-if="props.option.path">
              {{ props.option.path | join }}
            </small>
          </div>
        </div>
      </template>
    </b-autocomplete>
  </div>
</template>

<script>
import NotificationMixin from '@/components/NotificationMixin';
import regex from '@/lib/regex';

export default {
  filters: {
    join(value) {
      return value.join(', ');
    }
  },
  mixins: [NotificationMixin],
  data() {
    return {
      query: '', // Search query,
      suggestions: [],
      loading: false
    };
  },
  methods: {
    async onInput(value) {
      if (!value || value.length < 1) { return; }

      const escaped = regex.escape(value);
      try {
        this.loading = true;
        const result = await this.$axios.$get('/api/autocomplete', {
          params: {
            collection: 'zones', field: 'name', value: escaped, fields: ['_id', 'path']
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
      this.$emit('change', data);
    },
    highlight(value) {
      const escaped = regex.escape(this.query);
      return value.replace(
        new RegExp(escaped, 'gi'),
        str => `<strong>${str}</strong>`
      );
    }
  }
};
</script>
