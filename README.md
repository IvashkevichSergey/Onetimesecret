<h3>Features</h3>

<ul>
<li>FastAPI asynchronous backend</li>
<li>PostgreSQL as a database, SQLAlchemy as ORM, Alembic for migrations</li>
<li>Docker-compose integration</li>
<li>Data encryption by Fernet package</li>
</ul>

<h3>Launch</h3>

Install docker and docker-compose packages
<blockquote>pip install docker docker-compose</blockquote>
Run docker containers
<blockquote>docker-compose up --build</blockquote>

<h3>Endpoints</h3>

The <code>/generate</code> endpoint accepts a secret and a passphrase as a body params and 
returns the secret_key by which the secret can be obtained. Request body example:
<blockquote>{
    <br>"body": "Very mysterious secret",
    <br>"phrase": "hello"
<br>}</blockquote>
The <code>/secrets/{secret_key}</code> endpoint takes a secret_key as a query param and 
a passphrase as a body param and returns the secret. Request body example:
<blockquote>{
    <br>"phrase": "hello"
<br>}</blockquote>
To see interactive API documentation open <code>/docs</code>.
