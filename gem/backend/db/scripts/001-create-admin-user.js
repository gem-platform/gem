// Creat role for superuser
superuser = db.roles.insertOne({
    name: "Superuser",
    permissions: ["*"],
    priority: 9999
});

// Create admin
db.users.insertOne({
    name: "root",
    password: "root",
    roles: [ superuser.insertedId ]
});
