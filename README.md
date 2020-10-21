# Fullscratch JSON parser

勉強用にJSONパーサーを自作した。パースができることを目的にしたので、
コードが汚いかもというのとエラー処理をやりきってない。

## INSTALL

コピーしてください。

## HOW TO USE

    import myjson
    json_value = '{"a":"b"}'
    m = myjson.MyJson()
    print(m.parse(json_value))

### MyJson.parse(string)

与えられた文字列をパースして値を返します。

## LICENSE

MIT License.

