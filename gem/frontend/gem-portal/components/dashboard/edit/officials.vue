<template>
  <div>
    <!-- Name -->
    <b-field grouped>
      <!-- Name -->
      <b-field
        label="Name"
        expanded>
        <b-input
          v-model="name"
          placeholder="Name"
          size="is-large"/>
      </b-field>

      <!-- Form of adddress -->
      <b-field label="Address">
        <b-select
          v-model="formOfAddress"
          size="is-large">
          <option value="P">Das</option>
          <option value="M">Devi Dasi</option>
          <option value="S">Swami</option>
          <option value="G">Goswami</option>
          <option value="B">Bhakta</option>
        </b-select>
      </b-field>

      <!-- Appendage -->
      <b-field
        label="Detail (if necessary)"
        expanded>
        <b-input
          v-model="appendage"
          placeholder="Appendage"
          size="is-large"/>
      </b-field>
    </b-field>

    <!-- Email -->
    <b-field label="EMail">
      <b-input
        v-model="email"
        placeholder="EMail" />
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  mixins: [
    CrudEditComponentMixin({
      properties: [
        'name', 'formOfAddress', 'appendage', 'email'
      ]
    })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  }
};
</script>
