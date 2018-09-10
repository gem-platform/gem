export default class User {
  constructor(data) {
    this.id = data.id;
    this.name = data.name;
    this.roles = data.roles;
    this.permissions = data.permissions;
  }

  hasPermission(permission) {
    const isSuperUser = this.permissions.includes('*');
    const hasPermission = this.permissions.includes(permission);
    return isSuperUser || hasPermission;
  }
}
