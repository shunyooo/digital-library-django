# degital-library
研究室用の電子図書館、電子ビューワーWebサイト

# ANNOTATION
- `$` ホストマシン
- `SERVICE>` 該当のコンテナ内(例: `api>` はapiのコンテナ内を、 `>` のみの場合は任意のコンテナを表します。)

#### 

# BUILD & RUN

```shell
$ cd degital-library
$ docker-compose up
```

# ATTACH CONTAINER

```
$ docker-compose exec api bash
```
