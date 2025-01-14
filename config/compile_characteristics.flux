import "regexp"

PERIOD=2000ms
tagSelector=regexp.compile(v: v.stellantis_tag_regexp)

START = 2025-01-14T08:36:00Z
STOP = 2025-01-14T08:39:00Z

data_freq = from(bucket: "rfid")
  |> range(start: START, stop: STOP)
  |> filter(fn: (r) => r["_measurement"] == "read" and r._field == "frequency" and r.epc =~ tagSelector)
  |> map(fn: (r) => ({ r with _value: int(v: (int(v: r._value) - 865900) / 400) }))
  |> map(fn: (r) => ({ r with _value: if (r._value >= 5) then (r._value - 124 + 5) else r._value }))
  |> aggregateWindow(every: PERIOD, fn: distinct)
  |> filter(fn: (r) => exists r._value)
  |> aggregateWindow(every: PERIOD, fn: count)
  |> filter(fn: (r) => r._value > 0)
  |> set(key: "_field", value: "freq_count")  
  |> to(bucket: "stell_metrics")

data_rssi = from(bucket: "rfid")
  |> range(start: START, stop: STOP)
  |> filter(fn: (r) => r["_measurement"] == "read" and r._field == "value" and r.epc =~ tagSelector)
  //|> yield()

t0 = 2025-01-14T08:37:00Z
t1 = 2025-01-14T08:38:00Z

data_rssi
  |> aggregateWindow(every: PERIOD, fn: count)
  |> set(key: "_field", value: "rssi_count") 
  |> filter(fn: (r) => r._value > 0)
  |> to(bucket: "stell_metrics")

data_rssi
  |> aggregateWindow(every: PERIOD, fn: spread)
  |> set(key: "_field", value: "rssi_spread") 
  |> to(bucket: "stell_metrics")

data_rssi
  |> aggregateWindow(every: PERIOD, fn: max)
  |> set(key: "_field", value: "rssi_max") 
  |> to(bucket: "stell_metrics")

data_rssi
  |> aggregateWindow(every: PERIOD, fn: min)
  |> set(key: "_field", value: "rssi_min") 
  |> to(bucket: "stell_metrics")

data_rssi
  |> aggregateWindow(every: PERIOD, fn: stddev)
  |> set(key: "_field", value: "rssi_stdev") 
  |> to(bucket: "stell_metrics")
  |> set(key: "_field", value: "zone")  
  |> map(fn: (r) => ({ r with _value: if r._time > t1 then "far" else if  r._time > t0 then "med" else "near" }))
  |> to(bucket: "stell_metrics")
