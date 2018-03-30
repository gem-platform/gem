export default {
  socket: undefined,
  set(socket) {
    this.socket = socket;
  },
  send(command, data) {
    return new Promise((resolve, reject) => {
      this.socket.emit(command, data, (response) => {
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
          });
        },
        (error) => {
          reject(new Error(error.message || options.fail || 'Fail'));
        },
      );
    });
  },
};
