### Description

Extensible template for creating API services with account and JWT authentication support.

Features:

- Account registration, confirmation, authentication, refreshing, recovery.
- Account information model with `POST`, `PUT` and `GET` methods.
- Authentication with use of JWT tokens and scopes with compact account state modeling inside JWT payload.
- Basic locale detection, management and support for loading jinja2 templates for sending emails via SMTP.
- Argon2 as default password hashing algorithm.
- MongoDb via custom wrapper.
- Some initial work towards multiple email per account support.
- Verbose string based error reporting.
- Configuration via `config.json` file.

Notice:

- By default, the template is configured to allow unconfirmed users to pass authentication and receive a token
  with `type:access` scopes.
- If local mail server is running at port 25252, SMTP username and password settings are ignored.
- There are no default database constrains or indexes.
- Remember to overwrite the default JWT configuration keys.

### Run

It is possible to run the template without having a running MongoDb node or mail trap server. However, most calls will
result with an error.

Follow the instructions to use the project:

```shell
git clone https://github.com/milosob/template-api.git template-api
```

```shell
cd template-api
```

Modify the configuration file and apply the desired configuration.

```shell
vim config.json
```

#### Local

```shell
python -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install -e .
```

```shell
app --config config.json
```

#### Docker

To run a template with docker, build the image and run it with the mounted configuration file at `/config.json`.

```shell
docker build -t local/template-api .
```

```shell
docker run -v $(pwd)/config.json:/config.json:ro local/template-api
```
