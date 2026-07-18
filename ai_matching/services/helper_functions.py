import json

def profile_data_to_text(data):

    if not data:
        return ""

    text_parts = []

    for item in data:

        if isinstance(item, dict):

            for value in item.values():

                if isinstance(value, list):
                    text_parts.extend(
                        str(v) for v in value
                    )

                else:
                    text_parts.append(str(value))

        else:
            text_parts.append(str(item))

    return " ".join(text_parts)