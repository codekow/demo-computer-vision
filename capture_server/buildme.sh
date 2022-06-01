podman build -t pn-50.davenet.local:8080/repository/simplevis/capture-serv:$1 .
podman tag pn-50.davenet.local:8080/repository/simplevis/capture-serv:$1 pn-50.davenet.local:8080/repository/simplevis/capture-serv:latest
