import "experimental/array"
import ejson "experimental/json"
import "json"
import "http/requests"
import "influxdata/influxdb/schema"
import "regexp"

BASE_URL_="https://solid-space-zebra-wgpjr5qr7pq3gv-5000.app.github.dev/predict"

tagSelector=regexp.compile(v: v.stellantis_tag_regexp)

jsonStrings = from(bucket: "stell_metrics")
  |> range(start: -2s)
  |> filter(fn: (r) => r["_measurement"] == "read" and r.epc =~ tagSelector)
  |> map(fn: (r) => ({ r with _field: r._field + "_" + r.antenna }))
  |> drop(columns: ["antenna"])
  |> pivot(rowKey:["_time", "epc"], columnKey: ["_field"], valueColumn: "_value") 
  |> group()
  |> last(column: "_time")
  |> map(fn: (r) => ({ r with json: string(v: json.encode(v: r)) }))  
  |> keep(columns: ["json"])
//  |> yield(name: "aaa")
  |> findColumn(fn: (key) => true, column: "json")

response = requests.post(
                 url: BASE_URL_,
                 body: bytes(v: jsonStrings[0]),
                  headers: [
                      "Content-type": "application/json",
                      "Accept": "application/json"
                 ],
              )

array.from(rows: [{a: 1}])
|> map(
        fn: (r) => {
            jsonData = ejson.parse(data: response.body)

            return {
                far: jsonData.prediction.far,
                med: jsonData.prediction.med,
                near: jsonData.prediction.near
            }
        },
    )
|> map(fn: (r) => ({ r with _value: string(v: r.far) + " | " + string(v: r.med) + " | " + string(v: r.near) }))
|> yield(name: "response")
