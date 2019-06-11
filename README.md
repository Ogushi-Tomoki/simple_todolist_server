# simple_todo-server

## 概要
* TODO イベントを POST で登録　(JSON形式)
* TODO イベントを GET で取得 (JSON形式)
* CircleCI との連携による自動テストの実施


## API仕様
### イベント登録
```
# イベント登録 API request
POST /api/v1/todo
{"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}


# イベント登録 API response
# 成功
200 OK
{"status": "success", "message": "registered", "id": 1}

# 失敗
400 Bad Request
{"status": "failure", "message": "invalid date format"}
```

### イベント全取得
```
# イベント全取得 API request
GET /api/v1/todo

# イベント全取得 API response
200 OK
{"events": [
    {"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""},
    ...
]}
```

### イベント1件取得
```
# イベント1件取得 API request
GET /api/v1/todo/${id}

# イベント1件取得 API response
# 成功
200 OK
{"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}

# 失敗
404 Not Found
```