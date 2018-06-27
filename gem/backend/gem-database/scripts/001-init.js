// Create roles
superuser = db.roles.insertOne({name: "Superuser", permissions: ["*"]});

// Create users
db.users.insertOne({name: "root", password: "root", roles: [ superuser.insertedId ]});
