import "regexp"

option task = {name: "StellantisAggregatorTask", every: 2s}

PERIOD = task.every

tagSelector = regexp.compile(v: "EEA1")

data_freq =
    from(bucket: "rfid")
        |> range(start: -PERIOD)
        |> filter(
            fn: (r) =>
                r["_measurement"] == "read" and r._field == "frequency" and r.epc =~ tagSelector,
        )
        |> map(fn: (r) => ({r with _value: int(v: (int(v: r._value) - 865900) / 400)}))
        |> map(fn: (r) => ({r with _value: if r._value >= 5 then r._value - 124 + 5 else r._value}))
        |> aggregateWindow(every: PERIOD, fn: distinct, timeSrc: "_start")
        // Si dejamos el valor por defecto _stop, el encadenamiento del siguiente aggregateWindow siempre dará 0
        |> filter(fn: (r) => exists r._value)
        |> aggregateWindow(every: PERIOD, fn: count)
        |> filter(fn: (r) => r._value > 0)
        |> set(key: "_field", value: "freq_count")
        |> to(bucket: "stell_metrics")

data_rssi =
    from(bucket: "rfid")
        |> range(start: -PERIOD)
        |> filter(
            fn: (r) => r["_measurement"] == "read" and r._field == "value" and r.epc =~ tagSelector,
        )

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
