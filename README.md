diagram-object-recognizer
=====

Recognizer of objects in UML diagrams.

### Run with docker

Build image with all dependencies:
```shell script
docker image build -t flask_diagram .
```

Run container in bg:
```shell script
docker run -p 8080:8080 -d flask_diagram
```

Access to console of container:
```shell script
docker run -it flask_diagram
```


lsof -i -P -n | grep LISTEN