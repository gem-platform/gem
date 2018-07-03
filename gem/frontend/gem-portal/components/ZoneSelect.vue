<template>
  <div>
    <Autocomplete
      v-model="query"
      :fields="['_id', 'path']"
      collection="zones"
      field="name"
      @select="onSelected">
      <template slot-scope="{option: { name, path }}">
        <div class="media">
          <div class="media-content">
            <span v-html="highlight(name)"/>
            <br>
            <small v-if="path !== undefined && path.length > 0">
              {{ path | join }}
            </small>
          </div>
        </div>
      </template>
    </Autocomplete>
  </div>
</template>

<script>
import regex from '@/lib/regex';
import Autocomplete from '@/components/Autocomplete.vue';

export default {
  components: { Autocomplete },
  filters: {
    join(value) {
      return value.join(', ');
    }
  },
  props: {
    value: {
      type: String,
      default: undefined
    }
  },
  data() {
    return {
      query: this.value
    };
  },
  methods: {
    onSelected(data) {
      this.$emit('input', data);
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
