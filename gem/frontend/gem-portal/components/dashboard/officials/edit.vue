<template>
  <div>
    <!-- Name -->
    <b-field grouped>
      <!-- Name -->
      <b-field
        label="Name"
        expanded>
        <b-input
          v-model="entity.name"
          placeholder="Name"
          size="is-large"/>
      </b-field>

      <!-- Form of adddress -->
      <b-field label="Form">
        <b-select
          v-model="entity.formOfAddress"
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
        label="Appendage"
        expanded>
        <b-input
          v-model="entity.appendage"
          placeholder="Appendage"
          size="is-large"/>
      </b-field>
    </b-field>

    <!-- Email -->
    <b-field label="EMail">
      <b-input
        v-model="entity.email"
        placeholder="EMail" />
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  }
};
</script>
