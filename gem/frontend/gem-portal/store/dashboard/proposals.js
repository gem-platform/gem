import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'proposals',
  empty() {
    return {
      index: '', title: '', stage: '', content: ''
    };
  }
});
