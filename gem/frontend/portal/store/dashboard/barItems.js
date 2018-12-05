import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'barItems',
  empty() {
    return {
      name: '',
      description: '',
      image: ''
    };
  }
});
