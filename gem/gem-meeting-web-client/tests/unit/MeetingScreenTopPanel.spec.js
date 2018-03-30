import { mount } from '@vue/test-utils';
import GlobalMessage from '../../src/components/screens/MeetingScreenTopPanel.vue';

describe('MeetingScreenTopPanel.vue', () => {
  const wrapper = mount(GlobalMessage, { propsData: { title: 'title', subtitle: 'subtitle' } });

  it('displays specified message', () => {
    wrapper.setProps({
      title: 'Test Proposal',
      subtitle: 'Discussion',
    });
    expect(wrapper.find('.title').text()).toBe('Test Proposal');
    expect(wrapper.find('.subtitle').text()).toBe('Discussion');
  });
});
