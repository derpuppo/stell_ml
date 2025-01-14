import "experimental/array"
import "json"
import "http/requests"
import "influxdata/influxdb/schema"

BASE_URL_="https://solid-space-zebra-wgpjr5qr7pq3gv-5000.app.github.dev/predict"

jsonStrings = from(bucket: "stell_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "read")
  |> map(fn: (r) => ({ r with _field: r._field + "_" + r.antenna }))
  |> drop(columns: ["antenna"])
  |> pivot(rowKey:["_time", "epc"], columnKey: ["_field"], valueColumn: "_value") 
  |> group()
  |> top(n:1)
  |> map(fn: (r) => ({ r with json: string(v: json.encode(v: r)) }))  
  |> keep(columns: ["json"])
  |> yield(name: "aaa")
  |> findColumn(fn: (key) => true, column: "json")

response = requests.post(
                 url: BASE_URL_,
                 body: bytes(v: jsonStrings[0]),
                  headers: [
                      "Content-type": "application/json",
                      "Accept": "application/json"
                 ],
              )

array.from(rows: [{body: string(v: response.body)}])
|> yield(name: "response")
