"""
FollowMyTrips - Site Generator
================================
This script generates the full HTML site from the CITIES data below.
To add a new city, find the right country and add an entry to its cities list.
To add a new country, add a new entry to the COUNTRIES list.

Run with:  python3 generate_site.py
Output:    all HTML files in the same folder as this script

Photos:
  Put your photos in:  photos/<country-key>/<city-key>/photo1.jpg
  Up to 10 per city, any name, jpg/jpeg/png/webp all work.
  The gallery loads them automatically.

Requirements: Python 3.6+, no extra libraries needed.
"""

import os
import re

# ── CONFIGURATION ──────────────────────────────────────────────────────────────

SITE_NAME = "Follow My Trips"
AUTHOR = "Eriola"
LOGO = "@ET"
INSTAGRAM_URL = "https://www.instagram.com/placesdesignsbyet?igsh=MW1ob2t5dmRjZzY2dg=="
GISCUS = {
    "repo": "eritrouib/FollowMyTrips",
    "repo_id": "R_kgDOS21egg",
    "category": "Announcements",
    "category_id": "DIC_kwDOS21egs4C-6B0",
}

# ── COUNTRIES & CITIES ─────────────────────────────────────────────────────────
# Each country has:
#   key:    used for the HTML filename and photo folder name
#   name:   display name
#   flag:   emoji
#   photo:  Unsplash photo URL for the hero image
#   intro:  one paragraph shown at top of country page
#   cities: list of city dicts (see below)
#
# Each city has:
#   key:      used for anchor links and photo subfolder
#   name:     display name
#   status:   e.g. "Lived here", "Visited", "3 visits"
#   intro:    paragraph about the city (can be empty string for stubs)
#   tips:     list of {"label": ..., "text": ..., "neutral": True/False}
#   places:   list of {"name": ..., "desc": ...}
#   food:     list of {"name": ..., "desc": ...}
#
# Leave intro as "" and tips/places/food as [] for a stub city.

COUNTRIES = [
    {
        "key": "albania",
        "name": "Albania",
        "flag": "🇦🇱",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
        "intro": "I grew up in Elbasan and have been back many times. Albania has an ancient history that goes back well before any empire passed through it, and most visitors only scratch the surface. Fortified hilltop towns, Greek and Roman ruins, mountains that rival anywhere in Europe, an Ionian coast with fewer people than Greece in summer, and prices that are still very reasonable.",
        "cities": [
            {
                "key": "tirana",
                "name": "Tirana",
                "country_label": "Albania",
                "status": "Multiple visits",
                "intro": "Worth two days minimum. Walk from the Skenderbeu monument towards the University to see the ministries. The city has changed fast and keeps changing.",
                "tips": [
                    {"label": "Getting around", "text": "The city centre is walkable. Taxis are cheap but agree a price before you get in or use a metered one.", "neutral": True},
                    {"label": "Driving note", "text": "Be extra cautious even on highways, there can be animals or people crossing out of nowhere.", "neutral": True},
                ],
                "places": [
                    {"name": "Pazari i Ri (New Bazar)", "desc": "The place locals go for food and coffee. Good for lunch with traditional Albanian dishes. <a href='https://maps.app.goo.gl/M52wPaTV2fUDfRtf9' target='_blank' rel='noopener'>Map</a>"},
                    {"name": "The Pyramid", "desc": "A communist-era building that was Enver Hoxha's museum. Now a trendy space to climb on top of. <a href='https://maps.app.goo.gl/jdSySFiR7ohnWsJP8' target='_blank' rel='noopener'>Map</a>"},
                    {"name": "BunkArt 1 and 2", "desc": "Two museums inside actual Cold War bunkers. They show what life was like during communism. BunkArt 1 is built into a mountain, BunkArt 2 is in the centre. Both worth visiting."},
                    {"name": "Blloku", "desc": "The neighbourhood for cafes and nightlife. Was the exclusive area for Communist Party officials, now open to everyone. <a href='https://maps.app.goo.gl/vGF35rMSWUjhbDj48' target='_blank' rel='noopener'>Map</a>"},
                    {"name": "Mount Dajt cable car", "desc": "If you have time, the cable car up Mount Dajt gives good views over the city. <a href='https://maps.app.goo.gl/Qwj5Mcf9jePydmV69' target='_blank' rel='noopener'>Map</a>"},
                ],
                "food": [
                    {"name": "Mrizi i Zanave", "desc": "Well known restaurant with everything bio and a village atmosphere. On the expensive side but good quality. <a href='https://mriziizanave.al/' target='_blank' rel='noopener'>Website</a>"},
                ],
            },
            {
                "key": "elbasan",
                "name": "Elbasan",
                "country_label": "Albania",
                "status": "Grew up here",
                "intro": "One of the oldest towns in Albania. I grew up here so I know it well. It does not get many tourists but has a history going back to Roman times.",
                "tips": [],
                "places": [
                    {"name": "Elbasan Castle", "desc": "A well preserved castle with a long history in the centre of the old town. Worth a walk around. Do not eat at the restaurant inside the castle though, it is overpriced and not good. <a href='https://maps.app.goo.gl/fpMMeLCE9nrF2Ma18' target='_blank' rel='noopener'>Map</a>"},
                ],
                "food": [
                    {"name": "Taverna Attika", "desc": "Well known for Greek food. Great quality, many VIPs have eaten here. The owner lived in Greece for many years. Prices reflect the reputation but the food is genuinely good."},
                ],
            },
            {
                "key": "gjirokaster",
                "name": "Gjirokaster",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "UNESCO listed old town with a fortress that dominates the whole valley. Birthplace of both Enver Hoxha and Ismail Kadare, which tells you something about Albania's contradictions. The stone-paved streets are well preserved.",
                "tips": [],
                "places": [
                    {"name": "Gjirokaster Fortress", "desc": "The castle above the city is the reason to come. Good views over the valley from the top."},
                    {"name": "Old Bazaar", "desc": "The stone-paved bazaar quarter below the castle. Walk it in the morning before the tour groups arrive."},
                ],
                "food": [],
            },
            {
                "key": "pogradec",
                "name": "Pogradec",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "durres",
                "name": "Durres",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "Main port and nearest beach city to Tirana. Worth a stop on the way back to Tirana from the south rather than taking the direct road.",
                "tips": [],
                "places": [
                    {"name": "Roman Amphitheatre", "desc": "In the middle of the modern city, only rediscovered in the 1960s when someone was digging foundations. Enormous and largely unexcavated. One of the largest in the Balkans."},
                ],
                "food": [],
            },
            {
                "key": "sarande",
                "name": "Sarande",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "The main town on the Albanian Riviera. Good base for visiting Butrint and Ksamil. Corfu is visible from the promenade.",
                "tips": [
                    {"label": "Coastal restaurants in autumn", "text": "Restaurants in Sarande and the coast generally start closing from early October. Check ahead if visiting in autumn.", "neutral": True},
                ],
                "places": [
                    {"name": "Butrint", "desc": "Greek, Roman, Byzantine and Venetian ruins in a lagoon setting just outside Sarande. One of the most atmospheric archaeological sites in the Balkans and usually quiet."},
                    {"name": "Ksamil", "desc": "Small resort with turquoise water and small islands you can reach by a short boat ride. Gets crowded in August, beautiful in June or September."},
                ],
                "food": [],
            },
            {
                "key": "vlore",
                "name": "Vlore",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [
                    {"name": "Himara and the Riviera", "desc": "The coastal road between Vlore and Sarande passes through Himara and some of the best beaches on the Albanian Riviera. Drive it slowly."},
                ],
                "food": [],
            },
            {
                "key": "korce",
                "name": "Korce",
                "country_label": "Albania",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
    {
        "key": "greece",
        "name": "Greece",
        "flag": "🇬🇷",
        "photo": "https://images.unsplash.com/photo-1555993539-1732b0258235?w=1200&q=80",
        "intro": "I lived in Athens and have travelled widely across Greece. The islands get most of the attention but the mainland has some of the best food, history and landscapes in Europe.",
        "cities": [
            {
                "key": "athens",
                "name": "Athens",
                "country_label": "Greece",
                "status": "Lived here",
                "intro": "Athens is not just the Acropolis. That is obvious but still true. The city has neighbourhoods that feel completely different from each other and most visitors never get past the main sites. Give it at least four days.",
                "tips": [
                    {"label": "Looking for a place to rent?", "text": "I have a rental in Athens. If you are planning a longer stay or want a home rather than a hotel: <a href='https://eritrouib.github.io/RentAthens/' target='_blank' rel='noopener'>eritrouib.github.io/RentAthens</a>", "neutral": True},
                ],
                "places": [
                    {"name": "Anafiotika", "desc": "A cluster of white houses wedged into the north slope of the Acropolis rock. Looks like a Cycladic village dropped into the city. Quiet, cats everywhere. Most visitors walk straight past the entrance."},
                    {"name": "Monastiraki flea market", "desc": "Sunday mornings. Vinyl, old maps, vintage cameras, metalwork, junk. Get there before noon."},
                    {"name": "Exarchia", "desc": "Fine during the day and has some of the best cheap food in the city. Independent bookshops, political murals, very different atmosphere from the tourist areas."},
                    {"name": "Cape Sounion", "desc": "Temple of Poseidon on a cliff 70km from Athens. Take the KTEL coastal bus, the road hugs the cliffs the whole way. Go for sunset."},
                    {"name": "National Archaeological Museum", "desc": "One of the best museums in the world. The Antikythera Mechanism is there, a bronze computing device from 70BC that should not exist. Go and see it."},
                ],
                "food": [
                    {"name": "O Thanasis", "desc": "One of the most well known souvlaki restaurants in Athens, in Monastiraki. Decades old and consistently good. Go for the kebab and grilled meat. <a href='https://foodaroundathens.com/2026/03/13/the-legend-of-o-thanasis/' target='_blank' rel='noopener'>Read more</a>"},
                ],
            },
            {
                "key": "thessaloniki",
                "name": "Thessaloniki",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "kalamata",
                "name": "Kalamata",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "ioannina",
                "name": "Ioannina",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "corfu",
                "name": "Corfu",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "kefalonia",
                "name": "Kefalonia",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "chalcis",
                "name": "Chalcis",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "volos",
                "name": "Volos",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "methoni",
                "name": "Methoni",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "kastoria",
                "name": "Kastoria",
                "country_label": "Greece",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
    {
        "key": "uk",
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "photo": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&q=80",
        "intro": "I live in London and have travelled around the UK quite a bit. It is a much more varied country than people expect.",
        "cities": [
            {
                "key": "london",
                "name": "London",
                "country_label": "United Kingdom",
                "status": "Where I live",
                "intro": "London is enormous and people often see very little of it. Before I moved here I visited several times, and my European friends have all said the same thing: they expected one city and found something much bigger.",
                "tips": [
                    {"label": "Where to stay", "text": "Stay as close to the centre as your budget allows. The money you think you save on a cheaper hotel further out you will spend on TfL. Zones 1 and 2 is the sweet spot.", "neutral": False},
                    {"label": "Getting around", "text": "Tap your contactless bank card on the yellow readers. Do not buy paper single tickets, they cost almost double. If you have Revolut, use it. Most European banks charge transaction fees. Revolut does not.", "neutral": False},
                    {"label": "Museums are free", "text": "Almost all major museums have free entry. The Natural History Museum, V&A, British Museum, Tate Modern, National Gallery, Science Museum. All free. My favourites are the Natural History Museum and the Tate.", "neutral": True},
                ],
                "places": [
                    {"name": "Soho", "desc": "Where theatres, restaurants, bars and independent shops all run into each other. Best in the evening. <a href='https://www.visitlondon.com/things-to-do/london-areas/soho' target='_blank' rel='noopener'>visitlondon.com guide</a>"},
                    {"name": "West End theatres", "desc": "One of the best concentrations of theatre in the world. Book ahead for the big shows, or get same-day discounted tickets at the TKTS booth in Leicester Square."},
                    {"name": "Natural History Museum", "desc": "Free entry. The building alone is worth the visit. Give it half a day minimum."},
                    {"name": "Tate Modern", "desc": "Free entry. On the South Bank with good views across the Thames to St Paul's."},
                    {"name": "Richmond Park", "desc": "2,500 acres of ancient parkland with wild deer that walk past you at close range. Take the District line to Richmond."},
                    {"name": "Columbia Road Flower Market", "desc": "Sunday mornings only, done by 2pm. Walk to Broadway Market after for coffee and food stalls."},
                    {"name": "The Barbican", "desc": "1960s brutalist architecture with a fantastic arts centre, a conservatory full of tropical plants, and a lake. Very few tourists find it."},
                    {"name": "Hampstead Heath", "desc": "360 hectares of open land with ponds you can swim in. Parliament Hill has views across the whole city."},
                ],
                "food": [],
            },
            {
                "key": "brighton", "name": "Brighton", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "bath", "name": "Bath", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "bristol", "name": "Bristol", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "cardiff", "name": "Cardiff", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "birmingham", "name": "Birmingham", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "edinburgh", "name": "Edinburgh", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "glasgow", "name": "Glasgow", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "liverpool", "name": "Liverpool", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "manchester", "name": "Manchester", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "southampton", "name": "Southampton", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "poole", "name": "Poole", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "portsmouth", "name": "Portsmouth", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "worthing", "name": "Worthing", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "leeds", "name": "Leeds", "country_label": "United Kingdom", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
        ],
    },
    {
        "key": "spain",
        "name": "Spain",
        "flag": "🇪🇸",
        "photo": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1200&q=80",
        "intro": "I have been to Barcelona three times and travelled through Andalucia on several visits. Very different parts of the same country.",
        "cities": [
            {
                "key": "barcelona",
                "name": "Barcelona",
                "country_label": "Spain",
                "status": "3 visits",
                "intro": "I have been three times and would go back again. The Modernisme architecture is everywhere so you stop being surprised by it after a day. Each neighbourhood has a different feel and it is worth getting out of the centre.",
                "tips": [
                    {"label": "Get the Hola Barcelona Travel Card first", "text": "The <a href='https://www.holabarcelona.com/tickets/hola-bcn-barcelona-travel-card' target='_blank' rel='noopener'>Hola Barcelona Travel Card</a> covers metro, bus, tram, FGC trains and the airport on Metro L9 Sud from T1 and T2. Available for 2, 3, 4 or 5 consecutive days. On public buses show the card rather than tap it.", "neutral": False},
                    {"label": "On food", "text": "Do not sit at the restaurants on Las Ramblas. More expensive, smaller portions, not great food. Walk one street back and things improve immediately.", "neutral": True},
                ],
                "places": [
                    {"name": "Sagrada Familia", "desc": "I have not been inside but many people say it is worth it. Book tickets well ahead online."},
                    {"name": "Casa Mila and Casa Batllo", "desc": "Both on opposite sides of Passeig de Gracia. Walk between them and keep going towards Placa de Catalunya to reach La Rambla and the Mercat de la Boqueria."},
                    {"name": "Gothic Quarter and Cathedral", "desc": "Worth a proper walk around. Easy to spend a couple of hours just wandering the streets."},
                    {"name": "Parc Guell", "desc": "Beautiful park with good views over the city. The main zone requires a ticket, the rest is free. Go in the morning."},
                    {"name": "Montjuic Castle", "desc": "More worth it if the Font Magica fountain is running. Cable car up, check if it is included in your card at specific times."},
                    {"name": "Arc de Triomf to Ciutadella", "desc": "Walk from Arc de Triomf down the tree-lined boulevard and into Parc de la Ciutadella."},
                    {"name": "Barceloneta", "desc": "Walk along the beach. Plenty of restaurants along the seafront. Much better option than Las Ramblas."},
                    {"name": "Tibidabo", "desc": "Go for the view. The amusement park is very small. The lower funicular is covered by the Hola BCN card."},
                ],
                "food": [],
            },
            {
                "key": "seville",
                "name": "Seville",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "cordoba",
                "name": "Cordoba",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "granada",
                "name": "Granada",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "malaga",
                "name": "Malaga",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "ronda",
                "name": "Ronda",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "cadiz",
                "name": "Cadiz",
                "country_label": "Spain",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "gibraltar",
                "name": "Gibraltar",
                "country_label": "Gibraltar",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
    {
        "key": "italy",
        "name": "Italy",
        "flag": "🇮🇹",
        "photo": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&q=80",
        "intro": "Rome, Venice, Florence, Pisa. Notes being written up.",
        "cities": [
            {
                "key": "rome",
                "name": "Rome",
                "country_label": "Italy",
                "status": "Visited",
                "intro": "Rome needs more than a few days and most people give it fewer than that.",
                "tips": [
                    {"label": "Quick notes", "text": "Stay in Trastevere not the centre. Walk everywhere. Book the Borghese Gallery months ahead or you will not get in. Avoid eating anywhere that has photographs on the menu.", "neutral": True},
                ],
                "places": [],
                "food": [],
            },
            {
                "key": "venice", "name": "Venice", "country_label": "Italy", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "florence", "name": "Florence", "country_label": "Italy", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "pisa", "name": "Pisa", "country_label": "Italy", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
        ],
    },
    {
        "key": "balkans",
        "name": "Balkans",
        "flag": "🗺",
        "photo": "https://images.unsplash.com/photo-1555990538-1e3e3a4aef79?w=1200&q=80",
        "intro": "Kosovo, Montenegro and Croatia. Small distances, very different places.",
        "cities": [
            {
                "key": "prizren",
                "name": "Prizren",
                "country_label": "Kosovo",
                "status": "Visited",
                "intro": "Small city but very nice and good food. Worth a stop if you are in the region.",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "budva",
                "name": "Budva",
                "country_label": "Montenegro",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "dubrovnik",
                "name": "Dubrovnik",
                "country_label": "Croatia",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "split",
                "name": "Split",
                "country_label": "Croatia",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "ohrid",
                "name": "Ohrid",
                "country_label": "North Macedonia",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "struga",
                "name": "Struga",
                "country_label": "North Macedonia",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "skopje",
                "name": "Skopje",
                "country_label": "North Macedonia",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
    {
        "key": "central-europe",
        "name": "Central Europe",
        "flag": "🗺",
        "photo": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=1200&q=80",
        "intro": "Vienna, Budapest, Prague area, Switzerland, Benelux, France and Germany. A mix of very different cities.",
        "cities": [
            {
                "key": "vienna",
                "name": "Vienna",
                "country_label": "Austria",
                "status": "Visited",
                "intro": "I have been once. The museums are extraordinary, the food is good, and the city runs very smoothly.",
                "tips": [
                    {"label": "Getting around", "text": "Buy a Vienna City Card for public transport. Covers U-Bahn, trams and buses.", "neutral": False},
                    {"label": "Where to eat", "text": "I found a great place for pumpkin soup, goulash and schnitzel. We were lucky to get a table without a reservation but check ahead on busy days. <a href='https://maps.app.goo.gl/WwZLNAwAK8XFWGX59' target='_blank' rel='noopener'>Find it on Google Maps.</a>", "neutral": False},
                    {"label": "Schnitzel note", "text": "Eat Wiener Schnitzel at Figlmuller on Wollzeile, not the tourist branch near the opera.", "neutral": True},
                ],
                "places": [],
                "food": [],
            },
            {
                "key": "budapest",
                "name": "Budapest",
                "country_label": "Hungary",
                "status": "Visited",
                "intro": "Still one of the best value cities in Europe given how beautiful it is. Good for families, good for a trip with friends, I have done both.",
                "tips": [
                    {"label": "Thermal baths", "text": "Not a tourist gimmick, locals go too. Szechenyi is the most famous but Rudas or Lukacs are less crowded.", "neutral": True},
                    {"label": "For Sale Pub", "text": "A colleague recommended this and it was genuinely excellent. The walls are covered in notes and drawings left by visitors, ours should still be there. Live music at weekends. <a href='https://www.atlasobscura.com/places/for-sale-pub' target='_blank' rel='noopener'>More about it</a> or <a href='https://maps.app.goo.gl/j92aTwqY5Pp8eri76' target='_blank' rel='noopener'>map</a>.", "neutral": False},
                ],
                "places": [],
                "food": [],
            },
            {
                "key": "bratislava", "name": "Bratislava", "country_label": "Slovakia", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "brno", "name": "Brno", "country_label": "Czech Republic", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "heidelberg", "name": "Heidelberg", "country_label": "Germany", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "dusseldorf", "name": "Dusseldorf", "country_label": "Germany", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "zurich", "name": "Zurich", "country_label": "Switzerland", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "luxembourg", "name": "Luxembourg", "country_label": "Luxembourg", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "brussels", "name": "Brussels", "country_label": "Belgium", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "bruges", "name": "Bruges", "country_label": "Belgium", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "ghent", "name": "Ghent", "country_label": "Belgium", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "paris", "name": "Paris", "country_label": "France", "status": "Visited",
                "intro": "", "tips": [], "places": [], "food": [],
            },
            {
                "key": "eindhoven",
                "name": "Eindhoven",
                "country_label": "Netherlands",
                "status": "6-hour transit",
                "intro": "Everything was closed and it was cold (first of January). But I liked the city centre. Worth a proper visit.",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
    {
        "key": "turkey",
        "name": "Turkey",
        "flag": "🇹🇷",
        "photo": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80",
        "intro": "Visited Antalya and Side. The coast is beautiful and the history is remarkable.",
        "cities": [
            {
                "key": "antalya",
                "name": "Antalya",
                "country_label": "Turkey",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
            {
                "key": "side",
                "name": "Side",
                "country_label": "Turkey",
                "status": "Visited",
                "intro": "",
                "tips": [],
                "places": [],
                "food": [],
            },
        ],
    },
]

# ── HELPERS ────────────────────────────────────────────────────────────────────

INSTA_SVG = '<svg class="insta-icon" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'

def nav(current_file="index.html"):
    back = "" if current_file == "index.html" else "index.html"
    home_link = f'<li><a href="{back if back else "#"}">{"All countries" if back else "Home"}</a></li>' if back else ""
    # On index, comments anchor works. On country pages, link to #site-comments which is a general anchor
    comments_href = "#comments" if current_file == "index.html" else "../index.html#comments"
    return f"""<nav>
  <a class="nav-logo" href="index.html"><span class="et-logo">{LOGO}</span><span class="nav-site-name">{SITE_NAME}</span></a>
  <ul class="nav-links">
    {home_link}
    <li><a href="{comments_href}">Add a note</a></li>
  </ul>
  <a class="insta-link" href="{INSTAGRAM_URL}" target="_blank" rel="noopener">
    {INSTA_SVG}
    <span>Want to see my trips in watercolour? Visit my places&amp;designs page</span>
  </a>
</nav>"""

def footer():
    return f"""<footer>
  <div class="footer-logo">{LOGO}</div>
  <p class="footer-copy">&copy; <span id="yr"></span> {AUTHOR}. All rights reserved.</p>
  <p class="footer-sub">{SITE_NAME} &nbsp;&#183;&nbsp; Part of a personal portfolio</p>
  <p class="footer-credits">Photos courtesy of <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a> where not original photography.</p>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>"""

def giscus_block(term=None):
    g = GISCUS
    repo = g['repo']
    repo_id = g['repo_id']
    cat = g['category']
    cat_id = g['category_id']
    if term:
        mapping_attr = 'data-mapping="specific" data-term="' + term + '"'
        div_id = 'giscus-' + term
    else:
        mapping_attr = 'data-mapping="pathname"'
        div_id = 'giscus'
    return (
        '<div class="' + div_id + '"></div>\n'
        '<script src="https://giscus.app/client.js"\n'
        '  data-repo="' + repo + '" data-repo-id="' + repo_id + '"\n'
        '  data-category="' + cat + '" data-category-id="' + cat_id + '"\n'
        '  ' + mapping_attr + ' data-strict="0" data-reactions-enabled="1"\n'
        '  data-emit-metadata="0" data-input-position="bottom"\n'
        '  data-theme="preferred_color_scheme" data-lang="en" crossorigin="anonymous" async></script>'
    )

def photo_gallery(country_key, city_key):
    """Scans the photos folder at build time and embeds actual filenames in HTML."""
    folder = f"photos/{country_key}/{city_key}"
    out_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(out_dir, folder)
    exts = {'.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'}
    photos = []
    if os.path.isdir(folder_path):
        photos = sorted([
            f for f in os.listdir(folder_path)
            if os.path.splitext(f)[1] in exts
        ])[:10]
    if not photos:
        return ""
    imgs = "\n".join(
        f'''<img src="{folder}/{p}" alt="" loading="lazy" onclick="openLb('{city_key}',{i})">'''
        for i, p in enumerate(photos)
    )
    return f"""<div class="city-photos" id="gallery-{city_key}">{imgs}</div>
<div class="lightbox" id="lb-{city_key}">
  <span class="lightbox-close" onclick="closeLb('{city_key}')">&times;</span>
  <span class="lightbox-prev" onclick="lbNav('{city_key}',-1)">&#8249;</span>
  <img id="lb-img-{city_key}" src="" alt="">
  <span class="lightbox-next" onclick="lbNav('{city_key}',1)">&#8250;</span>
</div>"""

def tip_html(tip):
    cls = "tip-box neutral" if tip.get("neutral") else "tip-box"
    label_color = "" if tip.get("neutral") else ""
    return f"""<div class="{cls}">
  <p class="tip-label">{tip['label']}</p>
  <p class="tip-text">{tip['text']}</p>
</div>"""

def places_html(places, label="Places worth going"):
    if not places:
        return ""
    items = "\n".join(
        f'<div class="place"><p class="place-num">{str(i+1).zfill(2)}</p><p class="place-name">{p["name"]}</p><p class="place-desc">{p["desc"]}</p></div>'
        for i, p in enumerate(places)
    )
    return f'<p class="city-sub">{label}</p><div class="places-grid">{items}</div>'

def food_html(food):
    if not food:
        return ""
    items = "\n".join(
        f'<div class="place"><p class="place-num">{str(i+1).zfill(2)}</p><p class="place-name">{p["name"]}</p><p class="place-desc">{p["desc"]}</p></div>'
        for i, p in enumerate(food)
    )
    return f'<p class="city-sub">Where to eat</p><div class="places-grid">{items}</div>'

def city_section_html(city, country_key):
    is_stub = not city["intro"] and not city["tips"] and not city["places"] and not city["food"]
    country_label = city.get("country_label", "")
    heading_label = f'{city["name"]}, <em>{country_label}</em>' if country_label else city["name"]

    if is_stub:
        body = f'<div class="city-stub">Notes coming soon.</div>'
    else:
        tips = "\n".join(tip_html(t) for t in city["tips"])
        body = f"""
{('<p class="city-intro">' + city['intro'] + '</p>') if city['intro'] else ''}
{tips}
{places_html(city['places'])}
{food_html(city['food'])}"""

    gallery = photo_gallery(country_key, city["key"])
    comments = (
        '<p class="city-note-link">Have a tip about ' + city["name"] + '? '
        '<a href="../index.html#comments">Leave a note on the main page</a>.'
        '</p>'
    )

    return f"""<div class="city-section" id="{city['key']}">
  <span class="city-status">{city['flag'] if 'flag' in city else ''} {city['status']}</span>
  <h2 class="city-heading">{heading_label}</h2>
  {body}
  {gallery}
  {comments}
</div>"""

LIGHTBOX_JS = """
var lbData = {};
function openLb(cityKey, idx) {
  var lb = document.getElementById('lb-' + cityKey);
  lbData[cityKey] = lbData[cityKey] || {idx: 0};
  lbData[cityKey].idx = idx;
  var imgs = document.querySelectorAll('#gallery-' + cityKey + ' img');
  document.getElementById('lb-img-' + cityKey).src = imgs[idx].src;
  lb.classList.add('open');
}
function closeLb(cityKey) {
  document.getElementById('lb-' + cityKey).classList.remove('open');
}
function lbNav(cityKey, dir) {
  var imgs = document.querySelectorAll('#gallery-' + cityKey + ' img');
  var d = lbData[cityKey] || {idx: 0};
  d.idx = (d.idx + dir + imgs.length) % imgs.length;
  lbData[cityKey] = d;
  document.getElementById('lb-img-' + cityKey).src = imgs[d.idx].src;
}
// Close lightbox on background click
document.querySelectorAll('.lightbox').forEach(function(lb) {
  lb.addEventListener('click', function(e) {
    if (e.target === lb) lb.classList.remove('open');
  });
});
"""

PHOTO_LOADER_JS = ""  # Photos are now embedded at build time by photo_gallery()

# ── PAGE BUILDERS ──────────────────────────────────────────────────────────────

def build_page(html, filename, out_dir):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Written: {filename}")

def build_index(out_dir):
    cards = ""
    for c in COUNTRIES:
        teaser = c["intro"][:90] + "..." if len(c["intro"]) > 90 else c["intro"]
        city_count = len(c["cities"])
        cards += f"""
  <a class="city-card" href="{c['key']}.html" data-region="{c['key']}">
    <div style="background-image:url('{c['photo']}');" class="city-card-bg"></div>
    <div class="city-card-overlay"></div>
    <div class="city-card-body">
      <span class="city-card-status">{c['flag']} &nbsp; {city_count} {"city" if city_count == 1 else "cities"}</span>
      <div class="city-card-name">{c['name']}</div>
      <div class="city-card-teaser">{teaser}</div>
    </div>
  </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_NAME}</title>
<link rel="stylesheet" href="style.css">
<style>
.site-header{{padding:5rem 2rem 4rem;max-width:920px;margin:0 auto;border-bottom:1px solid var(--rule);}}
.site-header h1{{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5vw,3.5rem);font-weight:400;line-height:1.15;margin-bottom:1.2rem;}}
.site-header h1 em{{font-style:italic;color:var(--accent);}}
.site-header p{{font-size:1rem;color:var(--ink-mid);max-width:500px;line-height:1.75;}}
.city-grid{{max-width:1100px;margin:0 auto;padding:2rem 2rem 5rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem;}}
.city-card{{text-decoration:none;display:block;position:relative;overflow:hidden;border-radius:3px;aspect-ratio:4/3;}}
.city-card-bg{{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform 0.4s;}}
.city-card:hover .city-card-bg{{transform:scale(1.03);}}
.city-card-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.65) 0%,rgba(0,0,0,0.05) 55%,transparent 100%);transition:background 0.3s;}}
.city-card:hover .city-card-overlay{{background:linear-gradient(to top,rgba(0,0,0,0.75) 0%,rgba(0,0,0,0.15) 60%,transparent 100%);}}
.city-card-body{{position:absolute;bottom:1.2rem;left:1.3rem;right:1.3rem;color:#fff;}}
.city-card-status{{font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;font-weight:400;opacity:0.8;margin-bottom:0.3rem;display:block;}}
.city-card-name{{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:400;line-height:1.1;text-shadow:0 1px 4px rgba(0,0,0,0.4);}}
.city-card-teaser{{font-size:0.8rem;opacity:0;margin-top:0.4rem;line-height:1.45;transition:opacity 0.2s;}}
.city-card:hover .city-card-teaser{{opacity:0.9;}}
@media(max-width:600px){{.city-grid{{grid-template-columns:1fr 1fr;gap:0.8rem;padding:1.5rem 1.2rem 3rem;}}.city-card-name{{font-size:1.2rem;}}.site-header{{padding:3rem 1.2rem 2.5rem;}}}}
</style>
</head>
<body>
{nav("index.html")}
<header class="site-header">
  <h1>Cities I have been to.<br><em>The ones worth knowing.</em></h1>
  <p>I travel a lot and people ask me where to go and what to do. This is my running list. No fluff, just what I have found works.</p>
</header>
<div class="city-grid">
{cards}
</div>
<div id="comments" style="max-width:820px;margin:0 auto;padding:3rem 2rem 5rem;border-top:1px solid var(--rule);">
  <p style="font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink-light);font-weight:500;margin-bottom:1rem;">General notes</p>
  <h2 style="font-family:Playfair Display,serif;font-size:1.4rem;font-weight:400;margin-bottom:0.4rem;">Something to say?</h2>
  <p style="font-size:0.83rem;color:var(--ink-light);margin-bottom:1.5rem;">General feedback, suggestions, or a city you think I should visit.</p>
  {giscus_block()}
</div>
{footer()}
</body>
</html>"""
    build_page(html, "index.html", out_dir)

def build_country(country, out_dir):
    city_nav = " &nbsp;&#183;&nbsp; ".join(
        f'<a href="#{c["key"]}">{c["name"]}</a>' for c in country["cities"]
    )

    sections = "\n".join(
        city_section_html({**c, "flag": country["flag"]}, country["key"])
        for c in country["cities"]
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{country['name']} - {SITE_NAME}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{nav(country['key'] + '.html')}

<div class="dest-hero" style="background-image:url('{country['photo']}');">
  <div class="dest-hero-overlay"></div>
  <div class="dest-hero-label">
    <span class="dest-hero-sub">{country['flag']} &nbsp; {len(country['cities'])} cities</span>
    <div class="dest-hero-name">{country['name']}</div>
  </div>
</div>

<div class="country-nav">
  {city_nav}
</div>

<div class="country-body">
  <a class="dest-back" href="index.html">&#8592; All countries</a>
  <p style="font-size:1rem;color:var(--ink-mid);max-width:640px;margin:1.5rem 0 2rem;line-height:1.8;">{country['intro']}</p>

  {sections}

  <div id="site-comments" style="border-top:2px solid var(--rule);padding:3rem 0 2rem;">
    <p style="font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink-light);font-weight:500;margin-bottom:1rem;">General notes</p>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:400;margin-bottom:0.4rem;">Something to add about {country['name']}?</h2>
    <p style="font-size:0.83rem;color:var(--ink-light);margin-bottom:1.5rem;">General feedback about this page, or a city you think should be added.</p>
    {giscus_block("general-" + country["key"])}
  </div>
</div>

{footer()}
<script>
{LIGHTBOX_JS}
{PHOTO_LOADER_JS}
</script>
</body>
</html>"""
    build_page(html, f"{country['key']}.html", out_dir)

# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Generating site in: {out_dir}")

    # Create photo folders
    for country in COUNTRIES:
        for city in country["cities"]:
            folder = os.path.join(out_dir, "photos", country["key"], city["key"])
            os.makedirs(folder, exist_ok=True)

    print("\nBuilding index...")
    build_index(out_dir)

    print("\nBuilding country pages...")
    for country in COUNTRIES:
        build_country(country, out_dir)

    print(f"\nDone. {1 + len(COUNTRIES)} pages generated.")
    print("\nTo add photos:")
    print("  Drop images into photos/<country>/<city>/")
    print("  Name them 1.jpg, 2.jpg ... 10.jpg (or .png, .webp)")

if __name__ == "__main__":
    main()
