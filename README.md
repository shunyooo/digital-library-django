![image](https://user-images.githubusercontent.com/17490886/59975693-c23fd480-95f5-11e9-821e-fe7a3861f615.png)

研究室、少人数の仲間内で使うための電子図書館、電子ビューワーWebサイト



# DEV

**ANNOTATION**

- `$` ホストマシン
- `SERVICE>` 該当のコンテナ内(例: `api>` はapiのコンテナ内を、 `>` のみの場合は任意のコンテナを表す。)



## SETUP

```shell
$ cd digital-library
$ docker-compose up --build
```

web containerにattachしたいとき
```shell
$ docker-compose exec web bash
```



## DEBUG

起動から違う

```shell
$ cd digital-library
$ sh bin/docker-compose-build-run.sh
```

以下をコード中に挟む。[コマンド参考](https://qiita.com/makopo/items/170c939c79dcc5c89e12#ipdb%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E4%B8%80%E8%A6%A7)

```python
import ipdb; ipdb.set_trace();
```



# DEMO

[こちらにデモを置きました](http://silver.mind.meiji.ac.jp:65000/)（※ [パブー](http://p.booklog.jp/)の無料PDFを適当に入れました）

適当にいじって遊んでみてください。リンク切れは syunyooo(AT)gmail(dot)com へ。

