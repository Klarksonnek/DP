class ValueUtil:
    @staticmethod
    def detect_sensor_delays(events, window_size, threshold, value_attr_name,
                             delays_attr_name):
        for i in range(0, len(events)):
            event = events[i]

            values = event['measured'][value_attr_name]
            event[delays_attr_name] = 0

            for k in range(0, len(values) - window_size):
                first_value = values[k] - threshold
                second_value = values[k + window_size]

                if first_value > second_value:
                    event[delays_attr_name] = k
                    break

        return events

    @staticmethod
    def delays(events, delays_attr_name):
        out = []
        for event in events:
            out.append(event[delays_attr_name])

        return out
