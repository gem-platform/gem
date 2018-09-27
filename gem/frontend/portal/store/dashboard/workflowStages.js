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
      const action = item.actions[data.index];
      action.config = Object.assign({}, action.config, data.value);
    }
  }
});
