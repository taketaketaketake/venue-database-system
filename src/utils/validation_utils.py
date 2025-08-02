from thefuzz import fuzz
import logging

def deduplicate_events(events):
    try:
        deduplicated = []
        for event in events:
            is_duplicate = False
            for existing in deduplicated:
                name_similarity = fuzz.ratio(event['name'].lower(), existing['name'].lower())
                date_match = event['date'] == existing['date']
                if name_similarity > 90 and date_match:
                    is_duplicate = True
                    break
            if not is_duplicate:
                deduplicated.append(event)
        logging.info(f"Deduplicated {len(events)} events to {len(deduplicated)}")
        return deduplicated
    except Exception as e:
        logging.error(f"Deduplication error: {e}")
        return events
