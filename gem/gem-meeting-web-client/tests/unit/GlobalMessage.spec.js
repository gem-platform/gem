import { mount } from '@vue/test-utils';
import GlobalMessage from '../../src/components/GlobalMessage.vue';

describe('GlobalMessage.vue', () => {
  const wrapper = mount(GlobalMessage);

  it('displays default message', () => {
    expect(wrapper.find('.title').text()).toBe('Error');
    expect(wrapper.find('.subtitle').text()).toBe('Some error occurred');
  });

  it('displays specified message', () => {
    wrapper.setProps({
      title: 'Handshake Error',
      message: 'Wrong auth token',
    });
    expect(wrapper.find('.title').text()).toBe('Handshake Error');
    expect(wrapper.find('.subtitle').text()).toBe('Wrong auth token');
  });
});
