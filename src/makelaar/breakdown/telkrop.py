# %%
from bs4 import BeautifulSoup
import re

def extract_telkrop_data(html: str):
    soup = BeautifulSoup(html, "html.parser")
    listings = []
    base_url = "https://www.telkropmakelaars.nl"

    for obj in soup.select("li.al2woning"):
        try:
            # URL
            url_tag = obj.select_one("a.aanbodEntryLink")
            url = url_tag["href"] if url_tag else None
            if url and not url.startswith("http"):
                url = base_url + url

            # Address
            street_tag = obj.select_one("h3.street-address")
            city_tag = obj.select_one("span.locality")
            zip_tag = obj.select_one("span.postal-code")
            full_adres = f"{street_tag.text.strip()} in {city_tag.text.strip()} {zip_tag.text.strip()}" if street_tag and city_tag and zip_tag else None
            city = city_tag.text.strip() if city_tag else None

            # Price
            price = None
            price_tag = obj.select_one("span.kenmerk.koopprijs span.kenmerkValue")
            if price_tag:
                price_match = re.search(r"€\s?([\d\.,]+)", price_tag.text)
                if price_match:
                    price_str = price_match.group(1).replace(".", "").replace(",", ".")
                    try:
                        price = float(price_str)
                    except ValueError:
                        pass

            # Area
            area = None
            area_tag = obj.select_one("span.kenmerk.woonoppervlakte span.kenmerkValue")
            if area_tag:
                area_match = re.search(r"(\d+)\s*m", area_tag.text)
                if area_match:
                    area = int(area_match.group(1))

            # Number of rooms
            num_rooms = None
            rooms_tag = obj.select_one("span.kenmerk.aantalkamers span.kenmerkValue")
            if rooms_tag:
                rooms_match = re.search(r"(\d+)", rooms_tag.text)
                if rooms_match:
                    num_rooms = int(rooms_match.group(1))

            # Availability
            available = "Beschikbaar"
            status_tag = obj.select_one("span.objectstatusbanner")
            if status_tag:
                status_text = status_tag.text.strip().lower()
                if "verkocht" in status_text:
                    available = "Verkocht"
                elif "onder bod" in status_text:
                    available = "Onder bod"
                elif "nieuw" in status_text:
                    available = "Nieuw"

            listings.append({
                "full_adres": full_adres,
                "url": url,
                "city": city,
                "price": price,
                "area": area,
                "num_rooms": num_rooms,
                "available": available
            })
        except Exception:
            continue

    return listings


if __name__ == "__main__":
    from src.utils.get_url import get_html

    url ='https://www.telkropmakelaars.nl/aanbod/woningaanbod/AMSTERDAM/koop/'
    html = get_html(url)
    listings = extract_telkrop_data(html)
    for listing in listings:
        print(listing)