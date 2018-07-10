import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'roles',
  empty() {
    return { name: '', permissions: [] };
  }
});
