![image-20181106194500078](https://ws1.sinaimg.cn/large/006tNbRwgy1fwyj7i0lpwj30xu0cwh2s.jpg)

研究室用の電子図書館、電子ビューワーWebサイト



# DEV

**ANNOTATION**

- `$` ホストマシン
- `SERVICE>` 該当のコンテナ内(例: `api>` はapiのコンテナ内を、 `>` のみの場合は任意のコンテナを表す。)



## SETUP

```shell
$ cd degital-library
$ sh bin/docker-compose-build-run.sh
```

## ATTACH CONTAINER

```
$ docker-compose exec web bash
```
