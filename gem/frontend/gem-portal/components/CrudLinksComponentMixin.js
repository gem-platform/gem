export default {
  methods: {
    /**
     * Return link to edit page of entity
     * @param {string} id ID of the entity
     */
    linkToView(id) {
      const { entities } = this.$route.params;
      return `/dashboard/${entities}/${id}`;
    },

    /**
     * Return link to create page of entity
     */
    linkToCreate() {
      const { entities } = this.$route.params;
      return `/dashboard/${entities}/@new/edit`;
    },

    /**
     * Return link to edit page of entity
     */
    linkToEdit(id) {
      const { entities } = this.$route.params;
      return `/dashboard/${entities}/${id}/edit`;
    },

    /**
     * Return link to delete page
     */
    linkToDelete(id) {
      const { entities } = this.$route.params;
      return `/dashboard/${entities}/${id}/edit`;
    }
  }
};
