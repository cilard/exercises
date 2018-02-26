# Exercise 1
### Docker
- Use `Dockerfile`
- Script `getweather.py` must be in the same directory in order to be added to the Docker box
#### Build
`$ docker build -t weather:dev .`
#### Run
`$ docker run --rm -e OPENWEATHER_API_KEY="xxxxx" -e CITY_NAME="xxxxx" weather:dev`
### Ansible
- `site.yml` uses `docker_daemon_conf` - the two must be in the same directory
#### Run
`$ ansible-playbook -i "localhost," -c local site.yml`
