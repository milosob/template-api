### Description

This project serves as easy extendable template for development of api services with use of Python and FastAPI.

Things template does:

- Account registration, email confirmation, JWT stateless recovery, JWT refreshing.
- Account info model with `POST`, `PUT` and `GET` methods, easy extendable.
- Authentication with use of JWT tokens and scopes with compact account state modeling inside JWT payload.
- Basic locale detection, management and support for loading jinja2 templates for sending emails via SMTP.
- Argon2 as default password hashing algorithm.
- MongoDb based via custom wrapping on the driver.
- Some initial work towards multiple email per account support.
- Verbose string based error reporting.
- Configuration via `config.json` file.

Notice:

- By default, the template is configured to allow unconfirmed users to pass authentication and receive a token
  with `type: access` scopes.
- If local mail trap is running at port 25252, SMTP username and password settings are ignored.
- There are no default constrains or indexes, you need to supply your own.

### Run

It is possible to run the template without having a running MongoDb node or mail trap server. However, most calls with
result with an error. If you desire to work with the template you need a running MongoDb node and mail/trap server.

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
