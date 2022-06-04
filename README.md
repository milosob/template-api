#### Description

This project serves as easy extendable template for development of api services with use of Python and FastAPI.

Things template does:

- Account registration, email confirmation and JWT stateless recovery.
- Basic locale detection, management and support for loading templates for sending email.
- Authentication with use of JWT tokens and scopes, compact state modeling, etc.
- MongoDb support via custom wrapping on the driver.
- Configuration via `config.json` file.

Notice:

- By default, the template is configured to allow unconfirmed users to pass authentication and receive a token
  with `type: access` scopes.
- If local mail trap is running at port 25252, smtp username and password settings are ignored.

#### Run

```shell
git clone https://github.com/milosob/template-api.git template-api
```

```shell
cd template-api
```

```shell
python -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install -e .
```

Modify the configuration file and apply the desired configuration. It is possible to run the template without having a
running MongoDb node or mail trap server. However, most calls with result with an error.

```shell
app --config-path config.json
```

#### Docker

To run a template with docker, build the image and run it with the mounted configuration file at `/ config.json`.
