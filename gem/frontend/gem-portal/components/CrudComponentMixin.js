import CrudController from '@/lib/crud';

export default options => {
  const controller = new CrudController({
    ...options
  });

  return {
    computed: {
      entity() {
        return controller.entity({
          id: this.$route.params.id
        });
      }
    },
    methods: {
      async save() {
        await controller.submit({
          id: this.entity._id,
          data: this.entity
        });

        this.$router.push(controller.redirectUrl);
        this.$snackbar.open({ message: 'Proposal has been updated' });
      }
    },
    async fetch({ store, params, error }) {
      await controller.fetch({ store, id: params.id });
    },
    created() {
      controller.set({ store: this.$store });
    }
  };
};
