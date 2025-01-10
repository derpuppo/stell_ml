import "influxdata/influxdb/schema"

from(bucket: "stell_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "read")
//  |> group(columns: ["epc"])
  |> schema.fieldsAsCols() 
  |> filter(fn: (r) => r["rssi_count"] > 0)
