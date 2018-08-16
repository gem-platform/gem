import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'meetings',
  empty() {
    return {
      title: '', start: '', end: '', agenda: '', permissions: [], proposals: []
    };
  }
});
