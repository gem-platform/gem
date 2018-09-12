import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'users',
  empty() {
    return { name: '', password: '', roles: [] };
  }
});
