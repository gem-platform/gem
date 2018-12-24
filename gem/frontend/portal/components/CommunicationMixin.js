class CommunicationError extends Error {
  constructor(message, data) {
    super(message);
    this.name = 'CommunicationError';
    this.data = data;
  }
}

export default {
  methods: {
    send(command, data) {
      return new Promise((resolve, reject) => {
        this.$socket.emit(command, data, (response) => {
          if (response && response.success) {
            resolve(response);
          } else {
            reject(response);
          }
        });
      });
    },
    request(options) {
      return new Promise((resolve, reject) => {
        this.send(options.command, options.data).then(
          (success) => {
            resolve({
              message: success.message || options.success || 'Success',
              success: true,
              data: success
            });
          },
          (error) => {
            reject(new CommunicationError(error.message || options.fail || 'Fail', error));
          }
        );
      });
    }
  }
};

