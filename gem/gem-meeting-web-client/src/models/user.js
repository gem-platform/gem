export default class User {
  constructor(data) {
    this.id = data.id;
    this.name = data.name;
    this.roles = data.roles;
    this.permissions = data.permissions;
  }

  hasPermission(permission) {
    return this.permissions.includes(permission);
  }
}
