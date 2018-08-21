import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'workflowStages',
  empty() {
    return {
      name: '', description: ''
    };
  }
});
