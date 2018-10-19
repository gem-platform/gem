<template>
  <div>
    <!-- Name -->
    <b-field
      label="Name">
      <b-input
        v-model.trim="name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <!-- Description -->
    <b-field label="Description">
      <b-input
        id="description"
        v-model="description"
        type="textarea"
        placeholder="Description"/>
    </b-field>

    <!-- Image -->
    <b-field
      label="Image">
      <input
        id="file"
        ref="file"
        type="file"
        @change="handleFileUpload()">
      <button @click="submitFile()">Submit</button>
    </b-field>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';

export default {
  mixins: [
    CrudEditComponentMixin({ properties: ['name', 'description', 'image'] })
  ],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      file: ''
    };
  },
  methods: {
    handleFileUpload() {
      [this.file] = this.$refs.file.files;
    },
    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      this.$axios.post(
        '/bar/image', formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
        .then((res) => {
          if (res.data.success) {
            this.image = res.data.path;
          }
          console.log('SUCCESS!!', res.data.path);
        })
        .catch(() => {
          console.log('FAILURE!!');
        });
    }
  }
};
</script>
