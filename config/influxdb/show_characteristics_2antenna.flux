import "influxdata/influxdb/schema"

from(bucket: "stell_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "read")
  |> map(fn: (r) => ({ r with _field: r._field + "_" + r.antenna }))
  |> drop(columns: ["antenna"])
  |> pivot(rowKey:["_time", "epc"], columnKey: ["_field"], valueColumn: "_value") 
  |> group()
