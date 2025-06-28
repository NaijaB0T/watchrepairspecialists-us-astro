import json
import random

def enrich_specialist_data(input_path, output_path):
    with open(input_path, 'r') as f:
        specialists = json.load(f)

    description_templates = [
        "Discover {name}, a premier watch repair specialist in {city}, {state}. With a stellar rating of {rating} from {review_count} reviews, they offer exceptional service. Contact them at {phone} for your watch repair needs.",
        "For top-tier watch repair services in {city}, {state}, look no further than {name}. They boast an impressive {rating}-star rating from {review_count} satisfied customers. Reach out to them at {phone}.",
        "{name}, located in the heart of {city}, {state}, is a trusted name in watch repair. Their expertise is reflected in their {rating} rating from {review_count} reviews. Call {phone} to schedule a consultation.",
        "Seeking a reliable watch repair specialist? {name} in {city}, {state}, comes highly recommended with a {rating}-star rating from {review_count} clients. Their contact number is {phone}.",
        "The team at {name} in {city}, {state}, provides expert watch repair services. With a {rating} rating based on {review_count} reviews, you can trust them with your timepiece. Contact them at {phone}.",
        "In {city}, {state}, {name} is a standout choice for watch repair. They have earned a {rating}-star rating from {review_count} customers for their quality work. Give them a call at {phone}.",
        "Customers rave about {name} in {city}, {state}, giving them a {rating}-star rating from {review_count} reviews. For professional watch repair, they are a top choice. Contact them at {phone}.",
        "With a strong reputation in {city}, {state}, {name} is a go-to specialist for watch repairs. They have a {rating} rating from {review_count} reviews. You can reach them at {phone}.",
        "For those in {city}, {state}, {name} offers dependable watch repair services. Their {rating}-star rating from {review_count} reviews speaks to their quality. Call them at {phone} to learn more.",
        "{name} is a leading watch repair specialist in {city}, {state}, with a {rating} rating from {review_count} reviews. For all your watch service needs, contact them at {phone}."
    ]

    for specialist in specialists.values():
        template = random.choice(description_templates)
        review_count = specialist.get('review_count')
        address = specialist.get('address', {})
        if address is None:
            address = {}
        description = template.format(
            name=specialist.get('name', 'N/A'),
            city=address.get('city', 'N/A'),
            state=address.get('state', 'N/A'),
            rating=specialist.get('rating', 'N/A'),
            review_count=int(review_count) if review_count is not None else 0,
            phone=specialist.get('phone', 'N/A')
        )
        specialist['description'] = description

    with open(output_path, 'w') as f:
        json.dump(specialists, f, indent=4)

if __name__ == '__main__':
    enrich_specialist_data('src/data/specialists.json', 'src/data/specialists_enriched.json')
