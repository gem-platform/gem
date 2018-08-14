// Create roles
superuser = db.roles.insertOne({
    name: "Superuser",
    permissions: ["*"],
    priority: 9999
});

// Create users
db.users.insertOne({name: "root", password: "root", roles: [ superuser.insertedId ]});
