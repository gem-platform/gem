# Install
1. Install [docker](https://www.docker.com/get-docker)
2. Put your ssl keys into .keys folder. Folder should contain following files: `fullchain.pem`, `privkey.pem`, `chain.pem`. Check `web/envs/staging.conf` for additional information.
3. Build and run docker containers for specified environment:
```sh
docker-compose -f ./docker-compose.yml -f ./docker-compose.staging.yml up -d --build
```
4. Check containers status `docker-compose ps`. All of them should be in `healthy` status.