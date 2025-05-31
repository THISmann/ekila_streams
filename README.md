## ekila streams application readme.


### Install dependencies

```poetry install```
### Activate poetry virtualenvs

```poetry shell```

### Run Migrations

```poetry run python manage.py makemigrations```

```poetry run python manage.py migrate```

### Run the server
```poetry run python manage.py runserver```

### Go to the browser
```localhost:8000```


### relall
docker run --rm \
  -v $(pwd)/zap-reports:/zap/wrk:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:8030/admin -r zap_report.html

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image ekilastreams:latest
