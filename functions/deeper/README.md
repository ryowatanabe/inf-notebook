# コードの編集
main.pyを編集する
```python
BUCKETNAME = gcpのGCSのバケット名
FILENAME =　アップロードするファイル名
DEEPER_APIBASEURL = DEEPERのAPIのベースURL
DEEPER_APIVERSION =　DEEPERのAPIバージョン
DEEPER_APIKEY =　DEEPERのAPIキー
```

# デプロイ
ブラウザのコンソールからデプロイです

# 定期実行を設定
Cloud SchedulerとPub/Subを使用する

# APIテスト
```bash
python main.py -test # リソースファイル生成のテスト
python main.py -songs12 # EP:songsでレベル12のデータを取得
python main.py -data12 # EP:dataでレベル12のデータを取得
```

# サーバ起動
```bash
python main.py
python main.py -debug
```
