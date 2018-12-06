class FilterUtil:
    @staticmethod
    def only_valid_events(events):
        out = []

        for event in events:
            if event['valid_event']:
                out.append(event)
        return out

    @staticmethod
    def temperature_diff(events, min_value, max_value):
        out = []

        for event in events:
            temp_in = event['measured']['temperature_in_celsius'][0]
            temp_out = event['measured']['temperature_out_celsius'][0]

            if min_value <= abs(temp_in - temp_out) <= max_value:
                out.append(event)

        return out

    @staticmethod
    def temperature_out_max(events, max_value):
        out = []

        for event in events:
            temp_out = event['measured']['temperature_out_celsius'][0]

            if temp_out < max_value:
                out.append(event)

        return out

    @staticmethod
    def humidity(events, min_out_specific_humidity, min_diff, max_diff):
        out = []

        for event in events:
            specific_in = event['measured']['rh_in_specific_g_kg'][0]
            specific_out = event['measured']['rh_out_specific_g_kg'][0]

            if specific_out < min_out_specific_humidity:
                out.append(event)
                continue

            if min_diff <= abs(specific_out - specific_in) <= max_diff:
                out.append(event)

        return out

    @staticmethod
    def attribute(events, attribute_name, value):
        out = []

        for event in events:
            if event[attribute_name] == value:
                out.append(event)

        return out

    @staticmethod
    def attribute_exclude(events, attribute_name, value):
        out = []

        for event in events:
            if event[attribute_name] != value:
                out.append(event)

        return out

    @staticmethod
    def measured_values_not_empty(events, attributes):
        out = []

        for event in events:
            valid = True
            for key, value in event['measured'].items():
                if key in attributes and value == []:
                    valid = False

            if valid:
                out.append(event)

        return out