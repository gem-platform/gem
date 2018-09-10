# Install
1. Install [docker](https://www.docker.com/get-docker)
2. Put your ssl keys into .keys folder. Folder should contain following files: `fullchain.pem`, `privkey.pem`, `chain.pem`. Check `gem-web-client.staging.conf` for additional information.
3. Build and run docker containers for specified environment:
```sh
GEM_ENV=staging docker-compose up -d --build
```
4. Check containers status `docker ps`. All of them should be in `healthy` status.