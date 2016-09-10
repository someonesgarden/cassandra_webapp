# Cassandra Terminal Flask App

Dockerfile_DBを使ってCassandraのクラスターを作成し、Dockerfile_Terminalを使って、Cassandraを操作するFlaskウェブアプリケーションを作成する。
Flask側のサーバーは、brew、pip、cassandra driverそのほか、かなりのインストールが行われるのでDocker buildは時間がかかる。

## Dockerfile_Terminal_Centos、Dockerfile_Terminal_Debian
* cassandra_driver for pythonを利用して、Flaskアプリケーションから操作する
* Centos(yum)バージョンはuwsgiがうまく動いてないので、Debian版の方が調子がいい

### イメージを作成

`docker build -f ./Dockerfile_Terminal_Debian -t sog-cas .`

### コンテナを作成
`docker run --name cassandra_term -p 5000:5000 -p 9090:9090 -v $(pwd)/app/templates:/app/templates -d sog-cas`


### インストールされているpipの
`pip freeze`


### FLask Socket.IOでWeb Socketを実現している


参考
<http://qiita.com/nanakenashi/items/6497caf1c56c36f47be9>
<https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/templates/index.html>
