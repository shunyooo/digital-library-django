![image](https://user-images.githubusercontent.com/17490886/59975693-c23fd480-95f5-11e9-821e-fe7a3861f615.png)

**私的利用の範囲でPDFを共有し、閲覧するための電子図書館アプリ。**



# [Demo](http://silver.mind.meiji.ac.jp:65000/)

上記リンク先より（※ [パブー](http://p.booklog.jp/)の無料PDFを適当に入れました）

リンク切れの場合はIssueへ


# Feature

- [x] PDFアップロード
- [x] PDF（zip）ダウンロード
- [x] PDFブラウザ閲覧
- [x] タグ機能
- [x] 検索機能
  - [x] タイトル検索
  - [x] タグ検索
- [x] モバイル対応

| HOME                                                         | DETAIL                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src='http://ww2.sinaimg.cn/large/006tNc79gy1g54iwcn1zvj30u00ypkbi.jpg'/> | <img src='http://ww1.sinaimg.cn/large/006tNc79gy1g54irr7kfnj30u00y0aqb.jpg'/> |



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
