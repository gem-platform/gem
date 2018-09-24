import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'workflowStages',
  empty() {
    return {
      name: '',
      description: '',
      actions: []
    };
  },
  mutations: {
    setActionConfig(state, data) {
      const item = data.id === '@new'
        ? state.newItem
        : state.items[data.id];
      item.actions[data.index].config = data.value;
    }
  }
});
