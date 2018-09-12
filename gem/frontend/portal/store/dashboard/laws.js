import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'laws',
  empty() {
    return { index: '', title: '', content: '' };
  }
});
