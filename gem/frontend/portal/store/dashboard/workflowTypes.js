import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'workflowTypes',
  empty() {
    return {
      name: '', stages: []
    };
  }
});
