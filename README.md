![image-20181106194500078](https://ws1.sinaimg.cn/large/006tNbRwgy1fwyj7i0lpwj30xu0cwh2s.jpg)

研究室、少人数の仲間内で使うための電子図書館、電子ビューワーWebサイト

[[ユーザマニュアル]]



# DEV

**ANNOTATION**

- `$` ホストマシン
- `SERVICE>` 該当のコンテナ内(例: `api>` はapiのコンテナ内を、 `>` のみの場合は任意のコンテナを表す。)



## SETUP

```shell
$ cd degital-library
$ docker-compose up --build
```

web containerにattachしたいとき
```shell
$ docker-compose exec web bash
```



## DEBUG

起動から違う

```shell
$ cd degital-library
$ sh bin/docker-compose-build-run.sh
```

以下をコード中に挟む。[コマンド参考](https://qiita.com/makopo/items/170c939c79dcc5c89e12#ipdb%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E4%B8%80%E8%A6%A7)

```python
import ipdb; ipdb.set_trace();
```



