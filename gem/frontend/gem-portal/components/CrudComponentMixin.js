import CrudController from '@/lib/crud';

export default options => {
  const controller = new CrudController({
    apiPrefix: '/api/' + options.model + 's/',
    storePrefix: 'dashboard/' + options.model + 's/',
    idField: options.idField || '_id',
    fields: options.fields, //['_id', 'title', 'index', 'content'],
    redirectUrl: '/dashboard/' + options.model + 's'
  });

  //let realId = undefined;

  return {
    computed: {
      entities() {
        return this.$store.getters['dashboard/' + options.model + 's/all'];
      },
      entity() {
        return controller.entity({
          id: this.$route.params.id
        });
      },
      newUrl() {
        return '/dashboard/' + options.model + 's/@new/edit';
      },
      editUrl() {
        const proposalIndex = this.$route.params.id;
        return '/dashboard/' + options.model + 's/' + proposalIndex + '/edit';
      },
      deleteUrl() {
        const proposalIndex = this.$route.params.id;
        return '/dashboard/' + options.model + 's/' + proposalIndex + '/delete';
      }
    },
    methods: {
      async save() {
        await controller.save({
          id: this.entity._id,
          data: this.entity
        });

        this.$router.push(controller.redirectUrl);
        this.$snackbar.open({ message: 'Proposal has been updated' });
      },

      async remove() {
        await controller.remove({ id: this.entity._id });
        this.$router.push(controller.redirectUrl);
        this.$snackbar.open({ message: 'Proposal has been deleted' });
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
