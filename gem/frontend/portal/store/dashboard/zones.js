import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'zones',
  empty() {
    return {
      name: '', parent: undefined, officials: []
    };
  }
});
