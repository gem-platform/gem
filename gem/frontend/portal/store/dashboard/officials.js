import crudStore from '@/lib/crud/store';

export default crudStore({
  collection: 'officials',
  empty() {
    return {
      name: '', formOfAddress: '', email: '', secretary: false, gbc: false, appendage: ''
    };
  }
});
