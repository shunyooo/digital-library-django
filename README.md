![image-20181106194500078](https://ws1.sinaimg.cn/large/006tNbRwgy1fwyj7i0lpwj30xu0cwh2s.jpg)

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



# 動作画面

HOME

![image](https://user-images.githubusercontent.com/17490886/55667968-20360900-589e-11e9-83c0-0f113a174e0e.png)

詳細画面。タグを設定できます。

![image](https://user-images.githubusercontent.com/17490886/55667980-36dc6000-589e-11e9-9064-b6d3a428c149.png)

タグやタイトルで検索

![image](https://user-images.githubusercontent.com/17490886/55667986-4bb8f380-589e-11e9-8fd1-b848a3a06199.png)

ダウンロードしなくても、ブラウザ上で内容が確認できます。

![image](https://user-images.githubusercontent.com/17490886/55667996-5a9fa600-589e-11e9-8206-3f1247e6bae7.png)

