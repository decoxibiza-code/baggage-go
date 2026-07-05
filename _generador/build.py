# -*- coding: utf-8 -*-
"""
Generador estatico de BaggageGo Mallorca.
Produce paginas HTML individuales (ES / EN / DE) optimizadas para SEO:
titulo+meta unicos, canonical, hreflang, Open Graph, JSON-LD, breadcrumbs,
enlazado interno, sitemap.xml y robots.txt.
Ejecutar:  python build.py
Salida:    carpeta padre (Web BaggageGo/)
"""
import os, html, shutil

# ---------------------------------------------------------------- CONFIG
DOMAIN = "https://baggage-go.com"  # dominio real (comprado)
BRAND  = "BaggageGo"
PHONE_DISPLAY = "+34 600 000 000"  # <-- tu telefono real
WA = "34600000000"                 # <-- tu WhatsApp real (sin + ni espacios)
EMAIL = "hola@baggage-go.com"      # <-- confirma/crea este email real
CITY = "Palma de Mallorca"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LANGS = ["es", "en", "de"]

# ---------------------------------------------------------------- UI STRINGS
UI = {
 "es": {
   "nav": [("Servicios","#servicios"),("Zonas","#zonas"),("Cómo funciona","como-funciona"),
           ("Precios","precios"),("Hoteles","hoteles-y-partners"),("Guías","blog"),("Contacto","contacto")],
   "book":"Reservar","quote":"Pedir precio","cta_main":"Reservar mi entrega",
   "wa":"Pedir precio por WhatsApp","home":"Inicio","services_t":"Servicios","zones_t":"Zonas",
   "related_s":"Otros servicios","related_z":"Entrega de maletas por zonas","faq":"Preguntas frecuentes",
   "cta_band_t":"¿Listo para viajar ligero?","cta_band_p":"Reserva tu entrega de equipaje o pide presupuesto de mudanza. Respondemos en menos de una hora.",
   "foot_tag":"Entrega premium de equipaje y mudanzas exprés en toda Mallorca.",
   "foot_company":"Una empresa de TVM Events.","coverage":"Toda Mallorca",
   "hero_cta2":"Presupuesto de mudanza","insured":"Asegurado","allisland":"Toda la isla",
   "breadcrumb":"Estás en","need_t":"¿Qué necesitas?","send":"Enviar solicitud",
   "price_from":"desde","draft":"Web borrador · sustituir teléfono, email y precios antes de publicar.",
 },
 "en": {
   "nav": [("Services","#servicios"),("Areas","#zonas"),("How it works","how-it-works"),
           ("Prices","prices"),("Hotels","hotels-partners"),("Guides","blog"),("Contact","contact")],
   "book":"Book","quote":"Get price","cta_main":"Book my delivery",
   "wa":"Get price on WhatsApp","home":"Home","services_t":"Services","zones_t":"Areas",
   "related_s":"Other services","related_z":"Luggage delivery by area","faq":"Frequently asked questions",
   "cta_band_t":"Ready to travel light?","cta_band_p":"Book your luggage delivery or request a moving quote. We reply within the hour.",
   "foot_tag":"Premium luggage delivery and express moving across Mallorca.",
   "foot_company":"A TVM Events company.","coverage":"All of Mallorca",
   "hero_cta2":"Moving quote","insured":"Insured","allisland":"Whole island",
   "breadcrumb":"You are here","need_t":"What do you need?","send":"Send request",
   "price_from":"from","draft":"Draft site · replace phone, email and prices before going live.",
 },
 "de": {
   "nav": [("Leistungen","#servicios"),("Gebiete","#zonas"),("Ablauf","how-it-works"),
           ("Preise","prices"),("Hotels","hotels-partners"),("Ratgeber","blog"),("Kontakt","contact")],
   "book":"Buchen","quote":"Preis anfragen","cta_main":"Lieferung buchen",
   "wa":"Preis per WhatsApp","home":"Start","services_t":"Leistungen","zones_t":"Gebiete",
   "related_s":"Weitere Leistungen","related_z":"Gepäcklieferung nach Gebiet","faq":"Häufige Fragen",
   "cta_band_t":"Bereit, leicht zu reisen?","cta_band_p":"Buche deine Gepäcklieferung oder fordere ein Umzugsangebot an. Wir antworten innerhalb einer Stunde.",
   "foot_tag":"Premium-Gepäcklieferung und Express-Umzüge auf ganz Mallorca.",
   "foot_company":"Ein Unternehmen von TVM Events.","coverage":"Ganz Mallorca",
   "hero_cta2":"Umzugsangebot","insured":"Versichert","allisland":"Ganze Insel",
   "breadcrumb":"Sie sind hier","need_t":"Was brauchst du?","send":"Anfrage senden",
   "price_from":"ab","draft":"Entwurf · Telefon, E-Mail und Preise vor dem Livegang ersetzen.",
 },
}

# Ruta base de cada idioma
LANG_BASE = {"es":"", "en":"en/", "de":"de/"}
# Subcarpeta de servicios / zonas por idioma
SEG = {
 "es":{"serv":"servicios","zona":"zonas"},
 "en":{"serv":"services","zona":"areas"},
 "de":{"serv":"leistungen","zona":"gebiete"},
}
# Slugs de paginas info por idioma (para nav)
INFO_SLUG = {
 "como-funciona":{"es":"como-funciona","en":"how-it-works","de":"so-funktioniert-es"},
 "precios":{"es":"precios","en":"prices","de":"preise"},
 "hoteles-y-partners":{"es":"hoteles-y-partners","en":"hotels-partners","de":"hotels-partner"},
 "contacto":{"es":"contacto","en":"contact","de":"kontakt"},
 "blog":{"es":"guias","en":"guides","de":"ratgeber"},
}
SEG_BLOG = {"es":"guias","en":"guides","de":"ratgeber"}

# ---------------------------------------------------------------- SERVICIOS
# cada servicio: group id -> {slug{lang}, title{lang}, desc{lang}, h1{lang}, intro{lang}, secs[{h2,p,li[]}]{lang}, faq[{q,a}]{lang}}
SERVICES = [
 {
  "id":"aeropuerto",
  "slug":{"es":"entrega-maletas-aeropuerto","en":"airport-luggage-delivery","de":"flughafen-gepaeck-lieferung"},
  "icon":'<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M9 8V5h6v3M4 14h16"/>',
  "title":{"es":"Entrega de maletas aeropuerto PMI ↔ hotel | BaggageGo Mallorca",
           "en":"Airport luggage delivery PMI ↔ hotel | BaggageGo Mallorca",
           "de":"Flughafen-Gepäcklieferung PMI ↔ Hotel | BaggageGo Mallorca"},
  "desc":{"es":"Recogemos tu equipaje en el aeropuerto de Palma (PMI) y lo entregamos en tu hotel o villa. Llega con las manos libres. Servicio asegurado en toda Mallorca.",
          "en":"We collect your luggage at Palma airport (PMI) and deliver it to your hotel or villa. Arrive hands-free. Insured service across Mallorca.",
          "de":"Wir holen dein Gepäck am Flughafen Palma (PMI) ab und liefern es zu deinem Hotel oder deiner Villa. Komm mit freien Händen an. Versicherter Service auf ganz Mallorca."},
  "h1":{"es":"Entrega de maletas: aeropuerto PMI ↔ hotel o villa",
        "en":"Luggage delivery: PMI airport ↔ hotel or villa",
        "de":"Gepäcklieferung: Flughafen PMI ↔ Hotel oder Villa"},
  "intro":{"es":"Aterriza en Palma y olvídate de las maletas. Las recogemos en la terminal del aeropuerto PMI y las entregamos directamente en tu alojamiento —hotel, villa o apartamento— en cualquier punto de la isla.",
           "en":"Land in Palma and forget about your bags. We pick them up at PMI airport terminal and deliver them straight to your accommodation —hotel, villa or apartment— anywhere on the island.",
           "de":"Lande in Palma und vergiss dein Gepäck. Wir holen es am Terminal des Flughafens PMI ab und liefern es direkt zu deiner Unterkunft —Hotel, Villa oder Apartment— überall auf der Insel."},
  "secs":{
    "es":[("Cómo funciona la entrega desde el aeropuerto",
           "Reservas online indicando tu vuelo, número de maletas y el destino. Un conductor recoge el equipaje y lo lleva a tu alojamiento el mismo día, con seguimiento y seguro incluido.",
           ["Ideal para equipaje voluminoso: golf, bicicletas, tablas de surf.","Perfecto si viajas con niños o llegas en coche de alquiler.","Recogida también en el sentido inverso: hotel → aeropuerto para tu salida."]),
          ("¿Por qué no cargar tus maletas?",
           "Ganas tiempo y comodidad desde el primer minuto en Mallorca: sin colas en el parking, sin maleteros llenos, sin cargar peso bajo el sol.",[])],
    "en":[("How airport delivery works",
           "Book online with your flight, number of bags and destination. A driver collects your luggage and takes it to your accommodation the same day, with tracking and insurance included.",
           ["Ideal for bulky luggage: golf, bikes, surfboards.","Perfect if you travel with kids or arrive by rental car.","Also available the other way round: hotel → airport for your departure."]),
          ("Why carry your bags at all?",
           "Save time and enjoy comfort from your very first minute in Mallorca: no queues at the car park, no full boots, no lugging weight under the sun.",[])],
    "de":[("So funktioniert die Lieferung vom Flughafen",
           "Buche online mit deinem Flug, der Anzahl der Gepäckstücke und dem Ziel. Ein Fahrer holt dein Gepäck ab und bringt es am selben Tag zu deiner Unterkunft – mit Sendungsverfolgung und Versicherung.",
           ["Ideal für sperriges Gepäck: Golf, Fahrräder, Surfbretter.","Perfekt, wenn du mit Kindern reist oder mit dem Mietwagen ankommst.","Auch umgekehrt möglich: Hotel → Flughafen für deine Abreise."]),
          ("Warum überhaupt Gepäck schleppen?",
           "Spare Zeit und genieße Komfort von der ersten Minute auf Mallorca: keine Schlangen am Parkplatz, kein voller Kofferraum, kein Schleppen in der Sonne.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta la entrega de maletas desde el aeropuerto?","Desde 10 € por dos maletas puerta a puerta. El precio final depende de la zona de destino y del número de bultos; te lo confirmamos al instante por WhatsApp."),
          ("¿Entregáis el mismo día?","Sí. Con reserva anticipada garantizamos la entrega el mismo día de tu llegada en tu hotel o villa."),
          ("¿El equipaje va asegurado?","Sí, todos los envíos están asegurados y puedes seguir el estado de principio a fin.")],
    "en":[("How much is airport luggage delivery?","From €10 for two bags door to door. The final price depends on the destination area and number of items; we confirm instantly on WhatsApp."),
          ("Do you deliver the same day?","Yes. With advance booking we guarantee same-day delivery to your hotel or villa on your arrival day."),
          ("Is my luggage insured?","Yes, every shipment is insured and you can track its status from start to finish.")],
    "de":[("Was kostet die Gepäcklieferung vom Flughafen?","Ab 10 € für zwei Gepäckstücke von Tür zu Tür. Der Endpreis hängt vom Zielgebiet und der Anzahl der Stücke ab; wir bestätigen sofort per WhatsApp."),
          ("Liefert ihr am selben Tag?","Ja. Bei rechtzeitiger Buchung garantieren wir die Lieferung am Ankunftstag zu deinem Hotel oder deiner Villa."),
          ("Ist mein Gepäck versichert?","Ja, jede Sendung ist versichert und du kannst den Status von Anfang bis Ende verfolgen.")],
  },
 },
 {
  "id":"consigna",
  "slug":{"es":"consigna-equipaje-palma","en":"luggage-storage-palma","de":"gepaeckaufbewahrung-palma"},
  "icon":'<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V4h6v3M12 11v5M9 13h6"/>',
  "title":{"es":"Consigna de equipaje en Palma de Mallorca | BaggageGo",
           "en":"Luggage storage in Palma de Mallorca | BaggageGo",
           "de":"Gepäckaufbewahrung in Palma de Mallorca | BaggageGo"},
  "desc":{"es":"Guarda tus maletas de forma segura en Palma antes del check-in o después del check-out. Por horas o por días, con seguro. Reserva por WhatsApp.",
          "en":"Store your bags safely in Palma before check-in or after check-out. By the hour or by the day, insured. Book on WhatsApp.",
          "de":"Bewahre dein Gepäck sicher in Palma auf – vor dem Check-in oder nach dem Check-out. Stundenweise oder tageweise, versichert. Buchung per WhatsApp."},
  "h1":{"es":"Consigna de equipaje en Palma de Mallorca","en":"Luggage storage in Palma de Mallorca","de":"Gepäckaufbewahrung in Palma de Mallorca"},
  "intro":{"es":"¿Check-out temprano o vuelo nocturno? Guarda tus maletas con nosotros y aprovecha tus últimas horas en Mallorca sin cargar peso.",
           "en":"Early check-out or a night flight? Leave your bags with us and enjoy your last hours in Mallorca without carrying weight.",
           "de":"Früher Check-out oder Nachtflug? Lass dein Gepäck bei uns und genieße deine letzten Stunden auf Mallorca ohne Ballast."},
  "secs":{
    "es":[("Consigna flexible, por horas o días",
           "Deja tu equipaje de forma segura y recógelo cuando quieras. Un servicio pensado para el hueco entre el check-out y tu vuelo, o entre tu llegada y el check-in.",
           ["Custodia segura y asegurada.","Sin límite de tamaño: maletas grandes, bicis o material deportivo.","Combínalo con nuestra entrega para no volver a por las maletas."]),
          ("Consigna con entrega, la diferencia BaggageGo",
           "A diferencia de una consigna fija, nosotros también llevamos tu equipaje adonde lo necesites. Guardamos y entregamos.",[])],
    "en":[("Flexible storage, by the hour or by the day",
           "Leave your luggage securely and pick it up whenever you like. Designed for the gap between check-out and your flight, or between arrival and check-in.",
           ["Safe, insured custody.","No size limit: large suitcases, bikes or sports gear.","Combine it with our delivery so you never come back for your bags."]),
          ("Storage with delivery, the BaggageGo difference",
           "Unlike a fixed left-luggage point, we also take your bags wherever you need them. We store and we deliver.",[])],
    "de":[("Flexible Aufbewahrung, stundenweise oder tageweise",
           "Gib dein Gepäck sicher ab und hole es ab, wann du willst. Gedacht für die Lücke zwischen Check-out und Flug oder zwischen Ankunft und Check-in.",
           ["Sichere, versicherte Verwahrung.","Keine Größenbeschränkung: große Koffer, Fahrräder oder Sportausrüstung.","Kombiniere sie mit unserer Lieferung, damit du dein Gepäck nie wieder abholen musst."]),
          ("Aufbewahrung mit Lieferung – der BaggageGo-Unterschied",
           "Anders als eine feste Gepäckaufbewahrung bringen wir dein Gepäck auch dorthin, wo du es brauchst. Wir lagern und wir liefern.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta la consigna?","Desde 5 € por maleta y día. Consúltanos por franjas de pocas horas."),
          ("¿Dónde recogéis y entregáis?","En Palma y toda la isla. Podemos recoger en tu hotel y entregar en el aeropuerto o en otro alojamiento.")],
    "en":[("How much is storage?","From €5 per bag and day. Ask us about short few-hour slots."),
          ("Where do you collect and deliver?","In Palma and across the island. We can collect at your hotel and deliver to the airport or another accommodation.")],
    "de":[("Was kostet die Aufbewahrung?","Ab 5 € pro Gepäckstück und Tag. Frag uns nach kurzen Zeitfenstern von wenigen Stunden."),
          ("Wo holt ihr ab und liefert ihr?","In Palma und auf der ganzen Insel. Wir holen im Hotel ab und liefern zum Flughafen oder zu einer anderen Unterkunft.")],
  },
 },
 {
  "id":"ciclistas",
  "slug":{"es":"transporte-maletas-ciclistas","en":"cyclist-luggage-transfer","de":"gepaeck-transfer-radfahrer"},
  "icon":'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M6 17l4-8h5l3 8M10 9l2 8"/>',
  "title":{"es":"Transporte de equipaje para ciclistas y senderistas · Tramuntana | BaggageGo",
           "en":"Luggage transfer for cyclists & hikers · Tramuntana | BaggageGo",
           "de":"Gepäcktransfer für Radfahrer & Wanderer · Tramuntana | BaggageGo"},
  "desc":{"es":"Movemos tu equipaje y tu bici de hotel a hotel por la Serra de Tramuntana. Pedalea o camina ligero; nosotros nos ocupamos de las maletas.",
          "en":"We move your luggage and your bike from hotel to hotel across the Serra de Tramuntana. Ride or hike light; we handle the bags.",
          "de":"Wir transportieren dein Gepäck und dein Fahrrad von Hotel zu Hotel durch die Serra de Tramuntana. Fahr oder wandere leicht; wir kümmern uns um das Gepäck."},
  "h1":{"es":"Transporte de equipaje para ciclistas y senderistas","en":"Luggage transfer for cyclists and hikers","de":"Gepäcktransfer für Radfahrer und Wanderer"},
  "intro":{"es":"Recorres la Tramuntana en bici o a pie y cambias de hotel cada noche. Nosotros llevamos tu equipaje —y tu bicicleta— al siguiente alojamiento para que viajes sin peso.",
           "en":"You ride or hike the Tramuntana and change hotel every night. We take your luggage —and your bike— to the next accommodation so you travel weight-free.",
           "de":"Du fährst oder wanderst durch die Tramuntana und wechselst jede Nacht das Hotel. Wir bringen dein Gepäck – und dein Fahrrad – zur nächsten Unterkunft, damit du ohne Ballast reist."},
  "secs":{
    "es":[("Punto a punto por la Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... Coordinamos la recogida en tu hotel por la mañana y la entrega en el siguiente antes de que llegues.",
           ["Transporte de bicicletas de carretera y de montaña.","Coordinación con tu itinerario de etapas.","Servicio en temporada de ciclismo: primavera y otoño."]),
          ("Pensado para grupos y tour operadores",
           "Trabajamos con grupos ciclistas y tour operadores que organizan rutas por Mallorca. Un único contacto para todas las etapas.",[])],
    "en":[("Point to point across the Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... We coordinate pick-up at your hotel in the morning and drop-off at the next one before you arrive.",
           ["Road and mountain bike transport.","Coordinated with your stage itinerary.","Available in cycling season: spring and autumn."]),
          ("Built for groups and tour operators",
           "We work with cycling groups and tour operators running routes across Mallorca. One single contact for every stage.",[])],
    "de":[("Punkt zu Punkt durch die Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... Wir koordinieren die Abholung morgens im Hotel und die Lieferung im nächsten, bevor du ankommst.",
           ["Transport von Renn- und Mountainbikes.","Abgestimmt auf deine Etappen.","Verfügbar in der Radsaison: Frühling und Herbst."]),
          ("Für Gruppen und Reiseveranstalter gemacht",
           "Wir arbeiten mit Radgruppen und Reiseveranstaltern, die Touren über Mallorca organisieren. Ein einziger Ansprechpartner für alle Etappen.",[])],
  },
  "faq":{
    "es":[("¿Transportáis la bicicleta además del equipaje?","Sí, movemos maletas y bicicletas entre hoteles. Indícanos cuántas bicis y de qué tipo."),
          ("¿Trabajáis con grupos grandes?","Sí. Coordinamos itinerarios completos de varias etapas para grupos y agencias.")],
    "en":[("Do you transport the bike as well as luggage?","Yes, we move bags and bikes between hotels. Tell us how many bikes and what type."),
          ("Do you work with large groups?","Yes. We coordinate full multi-stage itineraries for groups and agencies.")],
    "de":[("Transportiert ihr das Fahrrad zusätzlich zum Gepäck?","Ja, wir bewegen Gepäck und Fahrräder zwischen Hotels. Sag uns, wie viele Räder und welcher Typ."),
          ("Arbeitet ihr mit großen Gruppen?","Ja. Wir koordinieren komplette mehrtägige Etappen für Gruppen und Agenturen.")],
  },
 },
 {
  "id":"mudanzas",
  "slug":{"es":"mudanzas-mallorca","en":"moving-mallorca","de":"umzug-mallorca"},
  "icon":'<path d="M3 13l2-6h11l3 4h2v5h-3M3 13v4h3M8 17h8"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>',
  "title":{"es":"Mudanzas exprés en Mallorca · BaggageGo Moving","en":"Express moving in Mallorca · BaggageGo Moving","de":"Express-Umzüge auf Mallorca · BaggageGo Moving"},
  "desc":{"es":"Mudanzas pequeñas y exprés en Mallorca: pisos, estudios y oficinas. Rápidas, cuidadas y aseguradas. Presupuesto sin compromiso.",
          "en":"Small and express moves in Mallorca: flats, studios and offices. Fast, careful and insured. Free quote.",
          "de":"Kleine und Express-Umzüge auf Mallorca: Wohnungen, Studios und Büros. Schnell, sorgfältig und versichert. Kostenloses Angebot."},
  "h1":{"es":"Mudanzas exprés en Mallorca","en":"Express moving in Mallorca","de":"Express-Umzüge auf Mallorca"},
  "intro":{"es":"¿Te mudas dentro de la isla? BaggageGo Moving hace mudanzas pequeñas y exprés de pisos, estudios y oficinas, con la misma fiabilidad y trato premium de nuestro servicio de equipaje.",
           "en":"Moving within the island? BaggageGo Moving handles small and express moves of flats, studios and offices, with the same reliability and premium care as our luggage service.",
           "de":"Ziehst du innerhalb der Insel um? BaggageGo Moving übernimmt kleine und Express-Umzüge von Wohnungen, Studios und Büros – mit derselben Zuverlässigkeit und dem Premium-Service unseres Gepäckdienstes."},
  "secs":{
    "es":[("Mudanzas rápidas y sin complicaciones",
           "Ideal para mudanzas de última hora, pisos de 1 a 3 habitaciones y pequeñas oficinas. Reserva ágil, embalaje opcional y entrega cuidada.",
           ["Mudanzas locales dentro de Mallorca.","Traslados puntuales de muebles y electrodomésticos.","Presupuesto claro y sin sorpresas."]),
          ("Para residentes y extranjeros que llegan a la isla",
           "Atendemos en español, inglés y alemán, algo clave para la gran comunidad de residentes extranjeros que se instala en Mallorca.",[])],
    "en":[("Fast, hassle-free moves",
           "Ideal for last-minute moves, 1 to 3-bedroom flats and small offices. Quick booking, optional packing and careful delivery.",
           ["Local moves within Mallorca.","One-off transport of furniture and appliances.","Clear quote, no surprises."]),
          ("For residents and newcomers to the island",
           "We serve in Spanish, English and German —key for the large community of foreign residents settling in Mallorca.",[])],
    "de":[("Schnelle, unkomplizierte Umzüge",
           "Ideal für kurzfristige Umzüge, Wohnungen mit 1 bis 3 Zimmern und kleine Büros. Schnelle Buchung, optionales Verpacken und sorgfältige Lieferung.",
           ["Lokale Umzüge innerhalb Mallorcas.","Einzeltransporte von Möbeln und Geräten.","Klares Angebot, keine Überraschungen."]),
          ("Für Einwohner und Neuankömmlinge auf der Insel",
           "Wir bedienen auf Spanisch, Englisch und Deutsch – entscheidend für die große Gemeinschaft ausländischer Einwohner, die sich auf Mallorca niederlässt.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta una mudanza pequeña?","Desde 300 € una mudanza local de un piso pequeño. Preparamos un presupuesto a medida según volumen, distancia y extras."),
          ("¿Hacéis mudanzas a la península o internacionales?","Coordinamos traslados a península e internacionales mediante grupaje; pídenos presupuesto.")],
    "en":[("How much is a small move?","From €300 for a local move of a small flat. We prepare a custom quote based on volume, distance and extras."),
          ("Do you do moves to the mainland or international?","We coordinate mainland and international moves via groupage; ask us for a quote.")],
    "de":[("Was kostet ein kleiner Umzug?","Ab 300 € für einen lokalen Umzug einer kleinen Wohnung. Wir erstellen ein individuelles Angebot nach Umfang, Entfernung und Extras."),
          ("Macht ihr Umzüge aufs Festland oder international?","Wir koordinieren Festland- und internationale Umzüge per Sammelladung; frag uns nach einem Angebot.")],
  },
 },
 {
  "id":"mercancias",
  "slug":{"es":"transporte-mercancias","en":"cargo-van-mallorca","de":"transporter-mit-fahrer"},
  "icon":'<rect x="3" y="7" width="11" height="9" rx="1"/><path d="M14 10h3l3 3v3h-6z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
  "title":{"es":"Transporte de mercancías y furgoneta con conductor en Mallorca | BaggageGo",
           "en":"Cargo van with driver & goods transport in Mallorca | BaggageGo",
           "de":"Transporter mit Fahrer & Warentransport auf Mallorca | BaggageGo"},
  "desc":{"es":"Transporte de mercancías, envíos voluminosos y furgoneta con conductor en toda Mallorca. Rápido, asegurado y con seguimiento, para empresas y particulares.",
          "en":"Goods transport, bulky deliveries and a cargo van with driver across Mallorca. Fast, insured and tracked, for businesses and individuals.",
          "de":"Warentransport, sperrige Lieferungen und ein Transporter mit Fahrer auf ganz Mallorca. Schnell, versichert und verfolgbar, für Unternehmen und Privatpersonen."},
  "h1":{"es":"Transporte de mercancías y furgoneta con conductor en Mallorca",
        "en":"Cargo van with driver and goods transport in Mallorca",
        "de":"Transporter mit Fahrer und Warentransport auf Mallorca"},
  "intro":{"es":"¿Necesitas mover mercancía, material o envíos voluminosos por la isla? Ponemos una furgoneta con conductor a tu disposición, con la fiabilidad y el trato profesional de una empresa de transporte establecida.",
           "en":"Need to move goods, materials or bulky deliveries around the island? We provide a cargo van with driver, with the reliability and professional service of an established transport company.",
           "de":"Musst du Waren, Material oder sperrige Lieferungen über die Insel bewegen? Wir stellen einen Transporter mit Fahrer bereit – mit der Zuverlässigkeit und dem professionellen Service eines etablierten Transportunternehmens."},
  "secs":{
    "es":[("Furgoneta con conductor para lo que necesites","Reparto de mercancía, entregas de última milla, material de eventos, mobiliario o envíos que no caben en un coche. Un solo contacto y facturación sencilla para empresas.",
           ["Servicio puntual o recurrente para empresas.","Entregas de última milla y paquetería voluminosa.","Cobertura en toda Mallorca, con seguro de mercancías."]),
          ("Para empresas y particulares","Trabajamos con comercios, eventos y particulares que necesitan transporte ágil sin contratar un camión completo.",[])],
    "en":[("A cargo van with driver for whatever you need","Goods distribution, last-mile deliveries, event materials, furniture or shipments that don't fit in a car. One contact and simple invoicing for businesses.",
           ["One-off or recurring service for businesses.","Last-mile deliveries and bulky parcels.","Island-wide coverage, with goods insurance."]),
          ("For businesses and individuals","We work with shops, events and individuals who need agile transport without hiring a full truck.",[])],
    "de":[("Ein Transporter mit Fahrer für alles, was du brauchst","Warenverteilung, Lieferungen auf der letzten Meile, Eventmaterial, Möbel oder Sendungen, die nicht ins Auto passen. Ein Ansprechpartner und einfache Abrechnung für Unternehmen.",
           ["Einmaliger oder wiederkehrender Service für Unternehmen.","Lieferungen auf der letzten Meile und sperrige Pakete.","Inselweite Abdeckung, mit Warenversicherung."]),
          ("Für Unternehmen und Privatpersonen","Wir arbeiten mit Geschäften, Events und Privatpersonen, die agilen Transport brauchen, ohne einen ganzen Lkw zu mieten.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta una furgoneta con conductor en Mallorca?","Depende del volumen, la distancia y el tiempo. Cuéntanos qué necesitas mover y te damos un presupuesto claro al momento."),
          ("¿Transportáis mercancía para empresas de forma recurrente?","Sí. Ofrecemos servicio puntual o rutas recurrentes con facturación mensual para comercios y empresas.")],
    "en":[("How much is a cargo van with driver in Mallorca?","It depends on volume, distance and time. Tell us what you need to move and we give you a clear quote right away."),
          ("Do you transport goods for businesses on a recurring basis?","Yes. We offer one-off service or recurring routes with monthly invoicing for shops and companies.")],
    "de":[("Was kostet ein Transporter mit Fahrer auf Mallorca?","Es hängt von Umfang, Entfernung und Zeit ab. Sag uns, was du bewegen musst, und wir geben dir sofort ein klares Angebot."),
          ("Transportiert ihr Waren für Unternehmen regelmäßig?","Ja. Wir bieten einmaligen Service oder wiederkehrende Routen mit monatlicher Abrechnung für Geschäfte und Unternehmen.")],
  },
 },
 {
  "id":"guardamuebles",
  "slug":{"es":"guardamuebles-mallorca","en":"storage-mallorca","de":"moebeleinlagerung-mallorca"},
  "icon":'<rect x="4" y="9" width="7" height="7" rx="1"/><rect x="13" y="9" width="7" height="7" rx="1"/><path d="M4 9l3-4h4l0 4M13 9l3-4h4l0 4"/>',
  "title":{"es":"Guardamuebles y almacenaje en Mallorca | BaggageGo",
           "en":"Storage and self storage in Mallorca | BaggageGo",
           "de":"Möbeleinlagerung und Lager auf Mallorca | BaggageGo"},
  "desc":{"es":"Guardamuebles y almacenaje seguro en Mallorca: muebles, enseres y stock. Por meses, con recogida y entrega. Ideal en mudanzas y reformas.",
          "en":"Secure storage and self storage in Mallorca: furniture, belongings and stock. Monthly, with pick-up and delivery. Ideal during moves and renovations.",
          "de":"Sichere Möbeleinlagerung und Lager auf Mallorca: Möbel, Hausrat und Warenbestand. Monatsweise, mit Abholung und Lieferung. Ideal bei Umzügen und Renovierungen."},
  "h1":{"es":"Guardamuebles y almacenaje en Mallorca","en":"Storage and self storage in Mallorca","de":"Möbeleinlagerung und Lager auf Mallorca"},
  "intro":{"es":"¿Necesitas espacio para tus muebles o tu stock durante una mudanza o una reforma? Guardamos tus enseres de forma segura y te los llevamos de vuelta cuando los necesites.",
           "en":"Need space for your furniture or stock during a move or a renovation? We store your belongings securely and bring them back whenever you need them.",
           "de":"Brauchst du Platz für deine Möbel oder deinen Warenbestand während eines Umzugs oder einer Renovierung? Wir lagern deine Sachen sicher und bringen sie zurück, wann immer du sie brauchst."},
  "secs":{
    "es":[("Almacenaje flexible por meses","Guarda muebles, cajas o stock el tiempo que necesites, con recogida y entrega a domicilio. La solución perfecta entre dos mudanzas o durante una reforma.",
           ["Custodia segura y asegurada.","Recogida y entrega a domicilio.","Combínalo con tu mudanza BaggageGo Moving."]),
          ("Para residentes y empresas","Ideal para residentes que se mudan y para comercios que necesitan guardar stock de temporada.",[])],
    "en":[("Flexible monthly storage","Store furniture, boxes or stock for as long as you need, with home pick-up and delivery. The perfect solution between two moves or during a renovation.",
           ["Safe, insured custody.","Home pick-up and delivery.","Combine it with your BaggageGo Moving move."]),
          ("For residents and businesses","Ideal for residents who are moving and for shops that need to store seasonal stock.",[])],
    "de":[("Flexible monatliche Einlagerung","Lagere Möbel, Kartons oder Warenbestand so lange du brauchst, mit Abholung und Lieferung nach Hause. Die perfekte Lösung zwischen zwei Umzügen oder während einer Renovierung.",
           ["Sichere, versicherte Verwahrung.","Abholung und Lieferung nach Hause.","Kombiniere sie mit deinem BaggageGo Moving Umzug."]),
          ("Für Einwohner und Unternehmen","Ideal für Einwohner, die umziehen, und für Geschäfte, die saisonalen Warenbestand lagern müssen.",[])],
  },
  "faq":{
    "es":[("¿Cómo se cobra el guardamuebles?","Por meses, según el volumen que necesites almacenar. Te damos un presupuesto a medida con recogida y entrega incluidas si las necesitas."),
          ("¿Recogéis y entregáis los muebles?","Sí. Recogemos en tu domicilio, almacenamos y te lo devolvemos cuando quieras, todo con el mismo equipo.")],
    "en":[("How is storage charged?","Monthly, based on the volume you need to store. We give you a custom quote with pick-up and delivery included if you need them."),
          ("Do you pick up and deliver the furniture?","Yes. We collect at your home, store it and return it whenever you like, all with the same team.")],
    "de":[("Wie wird die Einlagerung berechnet?","Monatsweise, je nach benötigtem Volumen. Wir geben dir ein individuelles Angebot mit Abholung und Lieferung, falls nötig."),
          ("Holt ihr die Möbel ab und liefert sie?","Ja. Wir holen bei dir zu Hause ab, lagern ein und bringen alles zurück, wann du willst – alles mit demselben Team.")],
  },
 },
 {
  "id":"bicicletas",
  "slug":{"es":"transporte-bicicletas","en":"bike-transport-mallorca","de":"fahrradtransport-mallorca"},
  "icon":'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M6 17l4-8h5l3 8M10 9l2 8"/>',
  "title":{"es":"Transporte de bicicletas en Mallorca | BaggageGo",
           "en":"Bike transport in Mallorca | BaggageGo",
           "de":"Fahrradtransport auf Mallorca | BaggageGo"},
  "desc":{"es":"Transporte de bicicletas en Mallorca: del aeropuerto al hotel y entre alojamientos. Para cicloturistas y grupos, con manipulación cuidadosa y seguro.",
          "en":"Bike transport in Mallorca: from the airport to your hotel and between accommodations. For cycling tourists and groups, with careful handling and insurance.",
          "de":"Fahrradtransport auf Mallorca: vom Flughafen zum Hotel und zwischen Unterkünften. Für Radtouristen und Gruppen, mit sorgfältiger Handhabung und Versicherung."},
  "h1":{"es":"Transporte de bicicletas en Mallorca","en":"Bike transport in Mallorca","de":"Fahrradtransport auf Mallorca"},
  "intro":{"es":"Mallorca es un paraíso ciclista. Llevamos tu bicicleta del aeropuerto a tu hotel y entre alojamientos, para que llegues y pedalees sin preocuparte del transporte.",
           "en":"Mallorca is a cyclist's paradise. We take your bike from the airport to your hotel and between accommodations, so you arrive and ride without worrying about transport.",
           "de":"Mallorca ist ein Radparadies. Wir bringen dein Fahrrad vom Flughafen zu deinem Hotel und zwischen Unterkünften, damit du ankommst und fährst, ohne dir Gedanken über den Transport zu machen."},
  "secs":{
    "es":[("Del aeropuerto al hotel y entre etapas","Transportamos bicicletas de carretera y de montaña, en caja o montadas, con manipulación cuidadosa. Coordinamos con tu itinerario por la Tramuntana.",
           ["Recogida en el aeropuerto PMI.","Traslado entre hoteles en rutas de varias etapas.","Servicio para grupos, clubes y tour operadores."]),
          ("Combínalo con tu equipaje","Movemos bici y maletas a la vez, para que viajes totalmente ligero.",[])],
    "en":[("From the airport to your hotel and between stages","We transport road and mountain bikes, boxed or assembled, with careful handling. We coordinate with your Tramuntana itinerary.",
           ["Pick-up at PMI airport.","Transfer between hotels on multi-stage routes.","Service for groups, clubs and tour operators."]),
          ("Combine it with your luggage","We move bike and bags together, so you travel completely light.",[])],
    "de":[("Vom Flughafen zum Hotel und zwischen Etappen","Wir transportieren Renn- und Mountainbikes, verpackt oder montiert, mit sorgfältiger Handhabung. Wir stimmen uns auf deine Tramuntana-Route ab.",
           ["Abholung am Flughafen PMI.","Transfer zwischen Hotels auf mehrtägigen Routen.","Service für Gruppen, Vereine und Reiseveranstalter."]),
          ("Kombiniere es mit deinem Gepäck","Wir bewegen Fahrrad und Gepäck gleichzeitig, damit du völlig leicht reist.",[])],
  },
  "faq":{
    "es":[("¿Transportáis la bici desde el aeropuerto?","Sí, recogemos tu bicicleta en el aeropuerto PMI y la entregamos en tu hotel o villa, montada o en caja."),
          ("¿Cuánto cuesta el transporte de una bicicleta?","Desde 18 € por bici y día. Para grupos y varias etapas preparamos un presupuesto a medida.")],
    "en":[("Do you transport the bike from the airport?","Yes, we collect your bike at PMI airport and deliver it to your hotel or villa, assembled or boxed."),
          ("How much is bike transport?","From €18 per bike and day. For groups and multiple stages we prepare a custom quote.")],
    "de":[("Transportiert ihr das Fahrrad vom Flughafen?","Ja, wir holen dein Fahrrad am Flughafen PMI ab und liefern es zu deinem Hotel oder deiner Villa, montiert oder verpackt."),
          ("Was kostet der Fahrradtransport?","Ab 18 € pro Rad und Tag. Für Gruppen und mehrere Etappen erstellen wir ein individuelles Angebot.")],
  },
 },
]

# ---------------------------------------------------------------- ZONAS
ZONES = [
 {"id":"palma","slug":"palma","name":"Palma",
  "es":{"title":"Entrega de maletas y consigna en Palma | BaggageGo","desc":"Entrega de equipaje, consigna y mudanzas exprés en Palma de Mallorca. Del aeropuerto o el puerto a tu hotel, sin cargar peso.",
        "h1":"Entrega de maletas y consigna en Palma","intro":"Palma concentra hoteles, cruceros y viajeros de negocios. Recogemos y entregamos tu equipaje por toda la ciudad y desde el aeropuerto PMI, y guardamos tus maletas cuando lo necesites.",
        "hi":["Del aeropuerto o la terminal de cruceros a tu hotel.","Consigna en el centro para tus últimas horas.","Mudanzas exprés dentro de la ciudad."]},
  "en":{"title":"Luggage delivery and storage in Palma | BaggageGo","desc":"Luggage delivery, storage and express moving in Palma de Mallorca. From the airport or port to your hotel, weight-free.",
        "h1":"Luggage delivery and storage in Palma","intro":"Palma concentrates hotels, cruises and business travellers. We collect and deliver your luggage across the city and from PMI airport, and store your bags whenever you need.",
        "hi":["From the airport or cruise terminal to your hotel.","City-centre storage for your last hours.","Express moves within the city."]},
  "de":{"title":"Gepäcklieferung und Aufbewahrung in Palma | BaggageGo","desc":"Gepäcklieferung, Aufbewahrung und Express-Umzüge in Palma de Mallorca. Vom Flughafen oder Hafen zu deinem Hotel, ohne Ballast.",
        "h1":"Gepäcklieferung und Aufbewahrung in Palma","intro":"Palma vereint Hotels, Kreuzfahrten und Geschäftsreisende. Wir holen und liefern dein Gepäck in der ganzen Stadt und vom Flughafen PMI und bewahren es auf, wann immer du willst.",
        "hi":["Vom Flughafen oder Kreuzfahrtterminal zu deinem Hotel.","Aufbewahrung im Zentrum für deine letzten Stunden.","Express-Umzüge innerhalb der Stadt."]}},
 {"id":"aeropuerto-pmi","slug":"aeropuerto-pmi","name":"Aeropuerto PMI",
  "es":{"title":"Entrega de equipaje desde el aeropuerto de Palma (PMI) | BaggageGo","desc":"Recogemos tu equipaje en el aeropuerto PMI y lo entregamos en tu hotel o villa el mismo día. Asegurado y con seguimiento.",
        "h1":"Entrega de equipaje desde el aeropuerto de Palma (PMI)","intro":"El aeropuerto de Palma es la puerta de entrada de millones de viajeros. Te esperamos en la terminal y llevamos tus maletas directamente a tu alojamiento.",
        "hi":["Recogida en llegadas del aeropuerto PMI.","Entrega el mismo día en cualquier zona.","También hotel → aeropuerto para tu salida."]},
  "en":{"title":"Luggage delivery from Palma airport (PMI) | BaggageGo","desc":"We collect your luggage at PMI airport and deliver it to your hotel or villa the same day. Insured, with tracking.",
        "h1":"Luggage delivery from Palma airport (PMI)","intro":"Palma airport is the gateway for millions of travellers. We meet you at the terminal and take your bags straight to your accommodation.",
        "hi":["Pick-up at PMI airport arrivals.","Same-day delivery to any area.","Also hotel → airport for your departure."]},
  "de":{"title":"Gepäcklieferung ab Flughafen Palma (PMI) | BaggageGo","desc":"Wir holen dein Gepäck am Flughafen PMI ab und liefern es am selben Tag zu deinem Hotel oder deiner Villa. Versichert, mit Sendungsverfolgung.",
        "h1":"Gepäcklieferung ab Flughafen Palma (PMI)","intro":"Der Flughafen Palma ist das Tor für Millionen Reisende. Wir erwarten dich am Terminal und bringen dein Gepäck direkt zu deiner Unterkunft.",
        "hi":["Abholung an der Ankunft des Flughafens PMI.","Lieferung am selben Tag in jedes Gebiet.","Auch Hotel → Flughafen für deine Abreise."]}},
 {"id":"soller","slug":"soller","name":"Sóller",
  "es":{"title":"Transporte de equipaje en Sóller y Port de Sóller | BaggageGo","desc":"Entrega de maletas y transporte para ciclistas y senderistas en Sóller y la Serra de Tramuntana. De hotel a hotel, sin peso.",
        "h1":"Transporte de equipaje en Sóller","intro":"Sóller, en plena Tramuntana, es parada obligada de ciclistas y senderistas. Movemos tu equipaje y tu bici entre hoteles del valle y la costa.",
        "hi":["Punto clave de rutas ciclistas de la Tramuntana.","Traslado de maletas de hotel a hotel.","Conexión con Deià, Valldemossa y Pollença."]},
  "en":{"title":"Luggage transfer in Sóller and Port de Sóller | BaggageGo","desc":"Luggage delivery and transfer for cyclists and hikers in Sóller and the Serra de Tramuntana. Hotel to hotel, weight-free.",
        "h1":"Luggage transfer in Sóller","intro":"Sóller, deep in the Tramuntana, is a must-stop for cyclists and hikers. We move your luggage and your bike between hotels in the valley and the coast.",
        "hi":["Key point on Tramuntana cycling routes.","Hotel-to-hotel luggage transfer.","Connection with Deià, Valldemossa and Pollença."]},
  "de":{"title":"Gepäcktransfer in Sóller und Port de Sóller | BaggageGo","desc":"Gepäcklieferung und Transfer für Radfahrer und Wanderer in Sóller und der Serra de Tramuntana. Hotel zu Hotel, ohne Ballast.",
        "h1":"Gepäcktransfer in Sóller","intro":"Sóller, mitten in der Tramuntana, ist ein Muss für Radfahrer und Wanderer. Wir bewegen dein Gepäck und dein Fahrrad zwischen Hotels im Tal und an der Küste.",
        "hi":["Schlüsselpunkt der Tramuntana-Radrouten.","Gepäcktransfer von Hotel zu Hotel.","Verbindung mit Deià, Valldemossa und Pollença."]}},
 {"id":"pollensa","slug":"pollensa","name":"Pollença",
  "es":{"title":"Equipaje para ciclistas en Pollença y Port de Pollença | BaggageGo","desc":"Transporte de equipaje y bicicletas en Pollença, meca del ciclismo del norte de Mallorca. De hotel a hotel por la Tramuntana.",
        "h1":"Equipaje y bicicletas en Pollença","intro":"Pollença y su puerto son base de equipos y aficionados al ciclismo. Llevamos tu equipaje y tu bici entre alojamientos para que solo pienses en pedalear.",
        "hi":["Base ciclista del norte de la isla.","Transporte de bicicletas entre etapas.","Ideal para grupos y campamentos de entrenamiento."]},
  "en":{"title":"Cyclist luggage in Pollença and Port de Pollença | BaggageGo","desc":"Luggage and bike transport in Pollença, the cycling mecca of northern Mallorca. Hotel to hotel across the Tramuntana.",
        "h1":"Luggage and bikes in Pollença","intro":"Pollença and its port are a base for cycling teams and enthusiasts. We carry your luggage and your bike between accommodations so you only think about riding.",
        "hi":["Cycling base in the north of the island.","Bike transport between stages.","Ideal for groups and training camps."]},
  "de":{"title":"Radfahrer-Gepäck in Pollença und Port de Pollença | BaggageGo","desc":"Gepäck- und Fahrradtransport in Pollença, dem Rad-Mekka im Norden Mallorcas. Hotel zu Hotel durch die Tramuntana.",
        "h1":"Gepäck und Fahrräder in Pollença","intro":"Pollença und sein Hafen sind Basis für Radteams und Enthusiasten. Wir bringen dein Gepäck und dein Fahrrad zwischen Unterkünften, damit du nur ans Fahren denkst.",
        "hi":["Rad-Basis im Norden der Insel.","Fahrradtransport zwischen Etappen.","Ideal für Gruppen und Trainingslager."]}},
 {"id":"alcudia","slug":"alcudia","name":"Alcúdia",
  "es":{"title":"Entrega de maletas en Alcúdia y Port d'Alcúdia | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles y apartamentos en Alcúdia. Cómodo para familias y estancias de playa.",
        "h1":"Entrega de maletas en Alcúdia","intro":"Alcúdia, en el norte, reúne grandes zonas hoteleras y de apartamentos familiares. Llevamos tu equipaje desde el aeropuerto para que empieces tus vacaciones sin cargar peso.",
        "hi":["Del aeropuerto PMI a tu hotel o apartamento.","Cómodo para familias con niños.","Consigna para el día de salida."]},
  "en":{"title":"Luggage delivery in Alcúdia and Port d'Alcúdia | BaggageGo","desc":"Luggage delivery from the airport to hotels and apartments in Alcúdia. Handy for families and beach stays.",
        "h1":"Luggage delivery in Alcúdia","intro":"Alcúdia, in the north, gathers large hotel and family apartment areas. We bring your luggage from the airport so you start your holiday weight-free.",
        "hi":["From PMI airport to your hotel or apartment.","Handy for families with kids.","Storage for departure day."]},
  "de":{"title":"Gepäcklieferung in Alcúdia und Port d'Alcúdia | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels und Apartments in Alcúdia. Praktisch für Familien und Strandaufenthalte.",
        "h1":"Gepäcklieferung in Alcúdia","intro":"Alcúdia im Norden vereint große Hotel- und Familienapartmentgebiete. Wir bringen dein Gepäck vom Flughafen, damit du deinen Urlaub ohne Ballast beginnst.",
        "hi":["Vom Flughafen PMI zu deinem Hotel oder Apartment.","Praktisch für Familien mit Kindern.","Aufbewahrung für den Abreisetag."]}},
 {"id":"andratx","slug":"andratx","name":"Andratx",
  "es":{"title":"Entrega de equipaje en Andratx y Port d'Andratx | BaggageGo","desc":"Servicio premium de entrega de maletas a villas y puertos deportivos en Andratx y el suroeste de Mallorca.",
        "h1":"Entrega de equipaje en Andratx","intro":"Andratx y su puerto concentran villas de lujo y náutica. Entregamos tu equipaje directamente en la villa o el yate, con el trato premium de una empresa de transfers VIP.",
        "hi":["Entrega directa en villas y puertos deportivos.","Servicio discreto y premium.","Ideal para estancias en el suroeste de la isla."]},
  "en":{"title":"Luggage delivery in Andratx and Port d'Andratx | BaggageGo","desc":"Premium luggage delivery to villas and marinas in Andratx and south-west Mallorca.",
        "h1":"Luggage delivery in Andratx","intro":"Andratx and its port concentrate luxury villas and yachting. We deliver your luggage straight to the villa or the yacht, with the premium care of a VIP transfer company.",
        "hi":["Direct delivery to villas and marinas.","Discreet, premium service.","Ideal for stays in the south-west of the island."]},
  "de":{"title":"Gepäcklieferung in Andratx und Port d'Andratx | BaggageGo","desc":"Premium-Gepäcklieferung zu Villen und Yachthäfen in Andratx und im Südwesten Mallorcas.",
        "h1":"Gepäcklieferung in Andratx","intro":"Andratx und sein Hafen vereinen Luxusvillen und Yachtsport. Wir liefern dein Gepäck direkt zur Villa oder Yacht – mit dem Premium-Service eines VIP-Transferunternehmens.",
        "hi":["Direkte Lieferung zu Villen und Yachthäfen.","Diskreter, premium Service.","Ideal für Aufenthalte im Südwesten der Insel."]}},
 {"id":"calvia","slug":"calvia","name":"Calvià",
  "es":{"title":"Entrega de maletas en Calvià, Palmanova y Santa Ponsa | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles y villas en Calvià y su costa (Palmanova, Portals, Santa Ponsa). Asegurado y con seguimiento.",
        "h1":"Entrega de maletas en Calvià","intro":"Calvià es el gran municipio turístico del suroeste, con Palmanova, Portals y Santa Ponsa. Llevamos tu equipaje del aeropuerto directamente a tu hotel o villa en toda su costa.",
        "hi":["Del aeropuerto PMI a tu hotel o villa.","Cobertura de Palmanova, Portals y Santa Ponsa.","Ideal para familias y estancias largas."]},
  "en":{"title":"Luggage delivery in Calvià, Palmanova and Santa Ponsa | BaggageGo","desc":"Luggage delivery from the airport to hotels and villas in Calvià and its coast (Palmanova, Portals, Santa Ponsa). Insured and tracked.",
        "h1":"Luggage delivery in Calvià","intro":"Calvià is the great tourist municipality of the south-west, with Palmanova, Portals and Santa Ponsa. We take your luggage from the airport straight to your hotel or villa along its coast.",
        "hi":["From PMI airport to your hotel or villa.","Coverage of Palmanova, Portals and Santa Ponsa.","Ideal for families and long stays."]},
  "de":{"title":"Gepäcklieferung in Calvià, Palmanova und Santa Ponsa | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels und Villen in Calvià und an seiner Küste (Palmanova, Portals, Santa Ponsa). Versichert und verfolgbar.",
        "h1":"Gepäcklieferung in Calvià","intro":"Calvià ist die große Tourismusgemeinde im Südwesten, mit Palmanova, Portals und Santa Ponsa. Wir bringen dein Gepäck vom Flughafen direkt zu deinem Hotel oder deiner Villa an der Küste.",
        "hi":["Vom Flughafen PMI zu deinem Hotel oder deiner Villa.","Abdeckung von Palmanova, Portals und Santa Ponsa.","Ideal für Familien und lange Aufenthalte."]}},
 {"id":"magaluf","slug":"magaluf","name":"Magaluf",
  "es":{"title":"Entrega de maletas en Magaluf | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles y apartamentos en Magaluf. Rápido y cómodo para empezar tus vacaciones sin cargar peso.",
        "h1":"Entrega de maletas en Magaluf","intro":"Magaluf concentra grandes hoteles y apartamentos en el suroeste. Recogemos tu equipaje en el aeropuerto y lo entregamos en tu alojamiento para que llegues con las manos libres.",
        "hi":["Del aeropuerto PMI a tu hotel o apartamento.","Cómodo para grupos y estancias de playa.","Consigna disponible para el día de salida."]},
  "en":{"title":"Luggage delivery in Magaluf | BaggageGo","desc":"Luggage delivery from the airport to hotels and apartments in Magaluf. Fast and easy so you start your holiday weight-free.",
        "h1":"Luggage delivery in Magaluf","intro":"Magaluf concentrates large hotels and apartments in the south-west. We collect your luggage at the airport and deliver it to your accommodation so you arrive hands-free.",
        "hi":["From PMI airport to your hotel or apartment.","Handy for groups and beach stays.","Storage available for departure day."]},
  "de":{"title":"Gepäcklieferung in Magaluf | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels und Apartments in Magaluf. Schnell und bequem, damit du deinen Urlaub ohne Ballast beginnst.",
        "h1":"Gepäcklieferung in Magaluf","intro":"Magaluf vereint große Hotels und Apartments im Südwesten. Wir holen dein Gepäck am Flughafen ab und liefern es zu deiner Unterkunft, damit du mit freien Händen ankommst.",
        "hi":["Vom Flughafen PMI zu deinem Hotel oder Apartment.","Praktisch für Gruppen und Strandaufenthalte.","Aufbewahrung für den Abreisetag verfügbar."]}},
 {"id":"santa-ponsa","slug":"santa-ponsa","name":"Santa Ponsa",
  "es":{"title":"Entrega de maletas en Santa Ponsa | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles, villas y campos de golf en Santa Ponsa. Asegurado, con seguimiento.",
        "h1":"Entrega de maletas en Santa Ponsa","intro":"Santa Ponsa combina hoteles, villas y golf en el suroeste. Llevamos tu equipaje —y tus palos de golf— del aeropuerto a tu alojamiento.",
        "hi":["Del aeropuerto PMI a tu hotel o villa.","Transporte de equipos de golf.","Zona de villas y residentes extranjeros."]},
  "en":{"title":"Luggage delivery in Santa Ponsa | BaggageGo","desc":"Luggage delivery from the airport to hotels, villas and golf resorts in Santa Ponsa. Insured, with tracking.",
        "h1":"Luggage delivery in Santa Ponsa","intro":"Santa Ponsa blends hotels, villas and golf in the south-west. We take your luggage —and your golf clubs— from the airport to your accommodation.",
        "hi":["From PMI airport to your hotel or villa.","Golf equipment transport.","Villa area with many foreign residents."]},
  "de":{"title":"Gepäcklieferung in Santa Ponsa | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels, Villen und Golfplätzen in Santa Ponsa. Versichert, mit Sendungsverfolgung.",
        "h1":"Gepäcklieferung in Santa Ponsa","intro":"Santa Ponsa verbindet Hotels, Villen und Golf im Südwesten. Wir bringen dein Gepäck – und deine Golfschläger – vom Flughafen zu deiner Unterkunft.",
        "hi":["Vom Flughafen PMI zu deinem Hotel oder deiner Villa.","Transport von Golfausrüstung.","Villengebiet mit vielen ausländischen Einwohnern."]}},
 {"id":"peguera","slug":"peguera","name":"Peguera",
  "es":{"title":"Entrega de maletas en Peguera | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles en Peguera, uno de los destinos favoritos del turismo alemán en Mallorca.",
        "h1":"Entrega de maletas en Peguera","intro":"Peguera es uno de los destinos preferidos del turismo alemán, con paseo peatonal y grandes hoteles. Recogemos tu equipaje en el aeropuerto y lo entregamos en tu hotel.",
        "hi":["Del aeropuerto PMI a tu hotel.","Atención en alemán, inglés y español.","Cómodo para estancias de playa."]},
  "en":{"title":"Luggage delivery in Peguera | BaggageGo","desc":"Luggage delivery from the airport to hotels in Peguera, one of the favourite destinations of German tourism in Mallorca.",
        "h1":"Luggage delivery in Peguera","intro":"Peguera is a favourite of German tourism, with a pedestrian promenade and large hotels. We collect your luggage at the airport and deliver it to your hotel.",
        "hi":["From PMI airport to your hotel.","Service in German, English and Spanish.","Handy for beach stays."]},
  "de":{"title":"Gepäcklieferung in Peguera | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels in Peguera, einem der beliebtesten Ziele deutscher Urlauber auf Mallorca.",
        "h1":"Gepäcklieferung in Peguera","intro":"Peguera ist ein Favorit deutscher Urlauber, mit Promenade und großen Hotels. Wir holen dein Gepäck am Flughafen ab und liefern es zu deinem Hotel.",
        "hi":["Vom Flughafen PMI zu deinem Hotel.","Service auf Deutsch, Englisch und Spanisch.","Praktisch für Strandaufenthalte."]}},
 {"id":"manacor","slug":"manacor","name":"Manacor",
  "es":{"title":"Transporte de equipaje y mudanzas en Manacor | BaggageGo","desc":"Entrega de equipaje, transporte y mudanzas exprés en Manacor y su costa (Porto Cristo, Cales de Mallorca). Asegurado.",
        "h1":"Transporte de equipaje y mudanzas en Manacor","intro":"Manacor, la segunda ciudad de Mallorca, y su costa este son zona de residentes y de villas. Ofrecemos entrega de equipaje, transporte y mudanzas exprés.",
        "hi":["Cobertura de Porto Cristo y Cales de Mallorca.","Mudanzas exprés para residentes.","Transporte de mercancía para comercios."]},
  "en":{"title":"Luggage transport and moving in Manacor | BaggageGo","desc":"Luggage delivery, transport and express moving in Manacor and its coast (Porto Cristo, Cales de Mallorca). Insured.",
        "h1":"Luggage transport and moving in Manacor","intro":"Manacor, Mallorca's second city, and its east coast are home to residents and villas. We offer luggage delivery, transport and express moving.",
        "hi":["Coverage of Porto Cristo and Cales de Mallorca.","Express moves for residents.","Goods transport for shops."]},
  "de":{"title":"Gepäcktransport und Umzüge in Manacor | BaggageGo","desc":"Gepäcklieferung, Transport und Express-Umzüge in Manacor und an seiner Küste (Porto Cristo, Cales de Mallorca). Versichert.",
        "h1":"Gepäcktransport und Umzüge in Manacor","intro":"Manacor, die zweitgrößte Stadt Mallorcas, und die Ostküste sind Heimat von Einwohnern und Villen. Wir bieten Gepäcklieferung, Transport und Express-Umzüge.",
        "hi":["Abdeckung von Porto Cristo und Cales de Mallorca.","Express-Umzüge für Einwohner.","Warentransport für Geschäfte."]}},
 {"id":"cala-dor","slug":"cala-dor","name":"Cala d'Or",
  "es":{"title":"Entrega de maletas en Cala d'Or | BaggageGo","desc":"Entrega de equipaje a hoteles, villas y puerto deportivo en Cala d'Or, en el sureste de Mallorca. Premium y asegurado.",
        "h1":"Entrega de maletas en Cala d'Or","intro":"Cala d'Or, con su puerto deportivo y sus calas, es un destino de villas y náutica en el sureste. Entregamos tu equipaje directamente en tu villa o barco.",
        "hi":["Entrega en villas y puerto deportivo.","Zona de calas del sureste.","Servicio discreto y premium."]},
  "en":{"title":"Luggage delivery in Cala d'Or | BaggageGo","desc":"Luggage delivery to hotels, villas and the marina in Cala d'Or, south-east Mallorca. Premium and insured.",
        "h1":"Luggage delivery in Cala d'Or","intro":"Cala d'Or, with its marina and coves, is a villa and boating destination in the south-east. We deliver your luggage straight to your villa or boat.",
        "hi":["Delivery to villas and the marina.","South-east coves area.","Discreet, premium service."]},
  "de":{"title":"Gepäcklieferung in Cala d'Or | BaggageGo","desc":"Gepäcklieferung zu Hotels, Villen und Yachthafen in Cala d'Or, im Südosten Mallorcas. Premium und versichert.",
        "h1":"Gepäcklieferung in Cala d'Or","intro":"Cala d'Or, mit seinem Yachthafen und seinen Buchten, ist ein Villen- und Bootsziel im Südosten. Wir liefern dein Gepäck direkt zu deiner Villa oder deinem Boot.",
        "hi":["Lieferung zu Villen und Yachthafen.","Buchtengebiet im Südosten.","Diskreter, premium Service."]}},
 {"id":"santanyi","slug":"santanyi","name":"Santanyí",
  "es":{"title":"Entrega de maletas y mudanzas en Santanyí | BaggageGo","desc":"Entrega de equipaje y mudanzas a villas en Santanyí y sus calas (Cala Llombards, Es Trenc). Zona premium del sureste.",
        "h1":"Entrega de maletas en Santanyí","intro":"Santanyí, con su mercado y sus calas vírgenes, es una de las zonas más exclusivas del sureste y muy querida por residentes alemanes. Entregamos equipaje y hacemos mudanzas a villas.",
        "hi":["Entrega en villas y fincas.","Cerca de Es Trenc y las calas del sur.","Popular entre residentes extranjeros."]},
  "en":{"title":"Luggage delivery and moving in Santanyí | BaggageGo","desc":"Luggage delivery and moving to villas in Santanyí and its coves (Cala Llombards, Es Trenc). Premium south-east area.",
        "h1":"Luggage delivery in Santanyí","intro":"Santanyí, with its market and unspoilt coves, is one of the most exclusive areas of the south-east and much loved by German residents. We deliver luggage and handle moves to villas.",
        "hi":["Delivery to villas and country estates.","Near Es Trenc and the southern coves.","Popular among foreign residents."]},
  "de":{"title":"Gepäcklieferung und Umzüge in Santanyí | BaggageGo","desc":"Gepäcklieferung und Umzüge zu Villen in Santanyí und seinen Buchten (Cala Llombards, Es Trenc). Premium-Gebiet im Südosten.",
        "h1":"Gepäcklieferung in Santanyí","intro":"Santanyí, mit seinem Markt und unberührten Buchten, ist eine der exklusivsten Gegenden im Südosten und bei deutschen Einwohnern sehr beliebt. Wir liefern Gepäck und übernehmen Umzüge zu Villen.",
        "hi":["Lieferung zu Villen und Fincas.","In der Nähe von Es Trenc und den südlichen Buchten.","Beliebt bei ausländischen Einwohnern."]}},
 {"id":"cala-ratjada","slug":"cala-ratjada","name":"Cala Ratjada",
  "es":{"title":"Entrega de maletas en Cala Ratjada | BaggageGo","desc":"Entrega de equipaje del aeropuerto a hoteles en Cala Ratjada, destino favorito del turismo alemán en el noreste de Mallorca.",
        "h1":"Entrega de maletas en Cala Ratjada","intro":"Cala Ratjada, en el noreste, es uno de los destinos preferidos del turismo alemán, con puerto y grandes hoteles. Recogemos tu equipaje en el aeropuerto y lo entregamos en tu hotel.",
        "hi":["Del aeropuerto PMI a tu hotel.","Atención en alemán, inglés y español.","Cobertura del noreste de la isla."]},
  "en":{"title":"Luggage delivery in Cala Ratjada | BaggageGo","desc":"Luggage delivery from the airport to hotels in Cala Ratjada, a favourite of German tourism in north-east Mallorca.",
        "h1":"Luggage delivery in Cala Ratjada","intro":"Cala Ratjada, in the north-east, is a favourite of German tourism, with a harbour and large hotels. We collect your luggage at the airport and deliver it to your hotel.",
        "hi":["From PMI airport to your hotel.","Service in German, English and Spanish.","Coverage of the north-east of the island."]},
  "de":{"title":"Gepäcklieferung in Cala Ratjada | BaggageGo","desc":"Gepäcklieferung vom Flughafen zu Hotels in Cala Ratjada, einem Favoriten deutscher Urlauber im Nordosten Mallorcas.",
        "h1":"Gepäcklieferung in Cala Ratjada","intro":"Cala Ratjada im Nordosten ist ein Favorit deutscher Urlauber, mit Hafen und großen Hotels. Wir holen dein Gepäck am Flughafen ab und liefern es zu deinem Hotel.",
        "hi":["Vom Flughafen PMI zu deinem Hotel.","Service auf Deutsch, Englisch und Spanisch.","Abdeckung des Nordostens der Insel."]}},
]

# ---------------------------------------------------------------- BLOG / GUÍAS
BLOG = [
 {"id":"bici","date":"2026-05-12","rel":["bicicletas","ciclistas"],
  "slug":{"es":"como-llevar-bicicleta-a-mallorca","en":"how-to-bring-your-bike-to-mallorca","de":"fahrrad-nach-mallorca-mitnehmen"},
  "title":{"es":"Cómo llevar tu bicicleta a Mallorca: guía práctica | BaggageGo","en":"How to bring your bike to Mallorca: practical guide | BaggageGo","de":"Fahrrad nach Mallorca mitnehmen: praktischer Ratgeber | BaggageGo"},
  "desc":{"es":"Guía para viajar con tu bici a Mallorca: facturación en el vuelo, alquiler y cómo mover la bicicleta entre hoteles de la Tramuntana sin complicaciones.","en":"A guide to travelling with your bike to Mallorca: flying with it, renting, and how to move your bike between Tramuntana hotels hassle-free.","de":"Ein Ratgeber für die Reise mit dem Fahrrad nach Mallorca: Flug, Miete und wie du dein Rad ohne Stress zwischen Tramuntana-Hotels bewegst."},
  "h1":{"es":"Cómo llevar tu bicicleta a Mallorca","en":"How to bring your bike to Mallorca","de":"Fahrrad nach Mallorca mitnehmen"},
  "intro":{"es":"Mallorca es uno de los mejores destinos ciclistas de Europa. Si vienes a rodar, esta guía te ayuda a decidir entre traer tu propia bici o alquilarla, y a moverla sin esfuerzo por la isla.","en":"Mallorca is one of Europe's best cycling destinations. If you are coming to ride, this guide helps you decide between bringing your own bike or renting, and moving it around the island effortlessly.","de":"Mallorca ist eines der besten Rad-Ziele Europas. Wenn du zum Fahren kommst, hilft dir dieser Ratgeber bei der Entscheidung zwischen eigenem Rad oder Miete und dabei, es mühelos über die Insel zu bewegen."},
  "secs":{
    "es":[("¿Traer tu bici o alquilarla?","Traer tu propia bicicleta te da comodidad y confianza, pero implica facturarla en el vuelo, con su coste y su embalaje. Alquilar evita el transporte aéreo pero limita la elección. Muchos ciclistas traen la suya para rutas largas por la Serra de Tramuntana.",[]),
          ("Facturar la bicicleta en el avión","Cada aerolínea tiene su política y su tarifa para bicicletas. Viaja con la bici desmontada y protegida en funda o maleta rígida, y confirma medidas y peso con tu compañía antes de volar.",[]),
          ("Muévela por la isla sin cargarla","Una vez en Mallorca, nosotros llevamos tu bicicleta del aeropuerto a tu hotel y entre alojamientos si haces rutas por etapas. Así ruedas ligero y tu equipaje te espera en el siguiente hotel.",[])],
    "en":[("Bring your bike or rent one?","Bringing your own bike gives you comfort and confidence, but means checking it in on the flight, with its cost and packing. Renting avoids air transport but limits your choice. Many cyclists bring their own for long routes across the Serra de Tramuntana.",[]),
          ("Checking your bike on the plane","Each airline has its own bike policy and fee. Travel with the bike disassembled and protected in a bag or hard case, and confirm dimensions and weight with your carrier before flying.",[]),
          ("Move it around the island without carrying it","Once in Mallorca, we take your bike from the airport to your hotel and between accommodations if you ride multi-stage routes. You ride light and your luggage waits at the next hotel.",[])],
    "de":[("Eigenes Rad mitbringen oder mieten?","Dein eigenes Rad gibt dir Komfort und Sicherheit, bedeutet aber Aufgabe im Flug, mit Kosten und Verpackung. Mieten vermeidet den Lufttransport, schränkt aber die Auswahl ein. Viele Radfahrer bringen ihr eigenes für lange Routen durch die Serra de Tramuntana.",[]),
          ("Das Fahrrad im Flugzeug aufgeben","Jede Fluggesellschaft hat ihre eigene Fahrradregel und Gebühr. Reise mit dem zerlegten und geschützten Rad in einer Tasche oder einem Hartschalenkoffer und bestätige Maße und Gewicht vor dem Flug.",[]),
          ("Beweg es über die Insel, ohne es zu tragen","Auf Mallorca bringen wir dein Rad vom Flughafen zu deinem Hotel und zwischen Unterkünften, wenn du mehrtägige Routen fährst. Du fährst leicht und dein Gepäck wartet im nächsten Hotel.",[])],
  }},
 {"id":"mudarse","date":"2026-04-20","rel":["mudanzas","guardamuebles"],
  "slug":{"es":"guia-para-mudarse-a-mallorca","en":"guide-to-moving-to-mallorca","de":"umzug-nach-mallorca-ratgeber"},
  "title":{"es":"Guía para mudarse a Mallorca (residentes y extranjeros) | BaggageGo","en":"Guide to moving to Mallorca (residents and expats) | BaggageGo","de":"Umzug nach Mallorca: Ratgeber für Auswanderer | BaggageGo"},
  "desc":{"es":"Todo lo que necesitas para mudarte a Mallorca: cómo organizar el traslado de tus muebles, el papeleo básico y opciones de guardamuebles mientras te instalas.","en":"Everything you need to move to Mallorca: how to organise your furniture transport, basic paperwork and storage options while you settle in.","de":"Alles für deinen Umzug nach Mallorca: wie du deinen Möbeltransport organisierst, grundlegende Formalitäten und Einlagerungsoptionen, während du dich einlebst."},
  "h1":{"es":"Guía para mudarse a Mallorca","en":"Guide to moving to Mallorca","de":"Umzug nach Mallorca: der Ratgeber"},
  "intro":{"es":"Mallorca recibe cada año a miles de nuevos residentes, sobre todo alemanes y británicos. Si vas a instalarte en la isla, esta guía te ayuda a planificar la mudanza paso a paso.","en":"Mallorca welcomes thousands of new residents every year, especially Germans and Britons. If you are settling on the island, this guide helps you plan your move step by step.","de":"Mallorca begrüßt jedes Jahr Tausende neue Einwohner, vor allem Deutsche und Briten. Wenn du dich auf der Insel niederlässt, hilft dir dieser Ratgeber, deinen Umzug Schritt für Schritt zu planen."},
  "secs":{
    "es":[("Planifica el traslado de tus muebles","Decide qué traes y qué compras aquí. Para el traslado desde la península o el extranjero, el grupaje (compartir camión) abarata mucho el coste. Dentro de la isla, una mudanza local es rápida y económica.",[]),
          ("Papeleo básico al llegar","Empadronamiento, NIE y alta de suministros son los primeros pasos. Conviene tener una dirección fija cuanto antes para agilizar los trámites.",[]),
          ("Guardamuebles mientras te instalas","Si aún no tienes vivienda definitiva, guardar tus muebles unos meses te da margen. Nosotros recogemos, almacenamos y te lo entregamos cuando tengas tu casa lista.",[])],
    "en":[("Plan your furniture transport","Decide what to bring and what to buy here. For transport from the mainland or abroad, groupage (sharing a truck) greatly reduces the cost. Within the island, a local move is fast and affordable.",[]),
          ("Basic paperwork on arrival","Town-hall registration (empadronamiento), NIE and utility contracts are the first steps. Having a fixed address as soon as possible speeds up the process.",[]),
          ("Storage while you settle in","If you don't have a permanent home yet, storing your furniture for a few months gives you breathing room. We collect, store and deliver it when your home is ready.",[])],
    "de":[("Plane deinen Möbeltransport","Entscheide, was du mitbringst und was du hier kaufst. Für den Transport vom Festland oder aus dem Ausland senkt Sammelladung (gemeinsamer Lkw) die Kosten stark. Auf der Insel ist ein lokaler Umzug schnell und günstig.",[]),
          ("Grundlegende Formalitäten bei der Ankunft","Anmeldung (Empadronamiento), NIE und Versorgungsverträge sind die ersten Schritte. Eine feste Adresse so früh wie möglich beschleunigt den Prozess.",[]),
          ("Einlagerung, während du dich einlebst","Wenn du noch kein endgültiges Zuhause hast, verschafft dir die Einlagerung deiner Möbel für einige Monate Spielraum. Wir holen ab, lagern und liefern, wenn dein Zuhause bereit ist.",[])],
  }},
 {"id":"sin-maletas","date":"2026-03-15","rel":["aeropuerto","consigna"],
  "slug":{"es":"viajar-por-mallorca-sin-cargar-maletas","en":"travel-mallorca-without-carrying-luggage","de":"mallorca-ohne-gepaeck-schleppen"},
  "title":{"es":"Viaja por Mallorca sin cargar las maletas | BaggageGo","en":"Travel around Mallorca without carrying your luggage | BaggageGo","de":"Mallorca bereisen, ohne dein Gepäck zu schleppen | BaggageGo"},
  "desc":{"es":"Descubre cómo disfrutar de Mallorca sin arrastrar el equipaje: entrega puerta a puerta, consigna y trucos para viajar ligero desde el aeropuerto.","en":"Discover how to enjoy Mallorca without dragging your bags: door-to-door delivery, storage and tips to travel light from the airport.","de":"Entdecke, wie du Mallorca genießt, ohne dein Gepäck zu schleppen: Lieferung von Tür zu Tür, Aufbewahrung und Tipps zum leichten Reisen."},
  "h1":{"es":"Viaja por Mallorca sin cargar las maletas","en":"Travel around Mallorca without carrying your luggage","de":"Mallorca bereisen, ohne dein Gepäck zu schleppen"},
  "intro":{"es":"Las vacaciones empiezan mejor sin arrastrar maletas por el aeropuerto y el parking. Te contamos cómo moverte por Mallorca con las manos libres de principio a fin.","en":"A holiday starts better without dragging bags through the airport and car park. Here is how to move around Mallorca hands-free from start to finish.","de":"Ein Urlaub beginnt besser, ohne Koffer durch Flughafen und Parkplatz zu schleppen. So bewegst du dich von Anfang bis Ende mit freien Händen über Mallorca."},
  "secs":{
    "es":[("Entrega de maletas del aeropuerto al hotel","En cuanto aterrizas, recogemos tu equipaje y lo llevamos directamente a tu hotel o villa. Tú vas directo a disfrutar, sin colas ni maleteros llenos.",[]),
          ("Consigna para las horas sin habitación","¿Check-out temprano o llegada antes del check-in? Guarda tus maletas por horas y aprovecha ese tiempo libre en la playa o el centro.",[]),
          ("Cambias de hotel sin cargar nada","Si recorres la isla o la Tramuntana, movemos tu equipaje de un hotel al siguiente. Viajas ligero y tus cosas te esperan al llegar.",[])],
    "en":[("Luggage delivery from the airport to your hotel","As soon as you land, we collect your luggage and take it straight to your hotel or villa. You go and enjoy, with no queues or full boots.",[]),
          ("Storage for the hours without a room","Early check-out or arrival before check-in? Store your bags by the hour and make the most of that free time at the beach or in the centre.",[]),
          ("Change hotels without carrying anything","If you tour the island or the Tramuntana, we move your luggage from one hotel to the next. You travel light and your things wait for you on arrival.",[])],
    "de":[("Gepäcklieferung vom Flughafen zum Hotel","Sobald du landest, holen wir dein Gepäck ab und bringen es direkt zu deinem Hotel oder deiner Villa. Du gehst genießen, ohne Schlangen oder vollen Kofferraum.",[]),
          ("Aufbewahrung für die Stunden ohne Zimmer","Früher Check-out oder Ankunft vor dem Check-in? Lagere dein Gepäck stundenweise und nutze die freie Zeit am Strand oder im Zentrum.",[]),
          ("Wechsle das Hotel, ohne etwas zu tragen","Wenn du die Insel oder die Tramuntana bereist, bewegen wir dein Gepäck von einem Hotel zum nächsten. Du reist leicht und deine Sachen warten bei der Ankunft.",[])],
  }},
]

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{--navy:#0A1E38;--blue:#12345E;--teal:#C6A15B;--teal-d:#93712F;--mint:#F1E8D5;--coral:#C6A15B;--coral-d:#B8924A;--amber:#D4A94B;--ink:#12233B;--muted:#5C6B7E;--bg:#FFFFFF;--soft:#FAF7F1;--line:#EAE3D5;--shadow:0 12px 34px rgba(10,30,56,.10);--shadow-lg:0 24px 60px rgba(10,30,56,.18);--r:14px;--r-lg:22px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2{font-family:'Playfair Display',Georgia,serif;line-height:1.14;letter-spacing:-.005em}h3,.brand{font-family:'Poppins','Inter',sans-serif;line-height:1.15;letter-spacing:-.02em}
a{color:inherit;text-decoration:none}.wrap{max-width:1160px;margin:0 auto;padding:0 22px}
.accent{color:var(--teal)}.coral{color:var(--coral)}section{padding:64px 0}
.eyebrow{display:inline-block;font-weight:600;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase;color:var(--teal-d);background:var(--mint);padding:6px 14px;border-radius:999px}
.lead{font-size:1.06rem;color:var(--muted);max-width:660px}.center{text-align:center;margin-left:auto;margin-right:auto}
.btn{display:inline-flex;align-items:center;gap:9px;font-weight:600;font-size:1rem;padding:13px 22px;border-radius:999px;border:0;cursor:pointer;transition:.2s;white-space:nowrap}
.btn svg{width:18px;height:18px}.btn-primary{background:var(--coral);color:#0A1E38;box-shadow:0 8px 22px rgba(198,161,91,.42)}.btn-primary:hover{background:var(--coral-d);transform:translateY(-2px)}
.btn-ghost{background:rgba(255,255,255,.14);color:#fff;border:1.5px solid rgba(255,255,255,.4)}.btn-ghost:hover{background:rgba(255,255,255,.24)}
.btn-teal{background:var(--navy);color:var(--teal);box-shadow:0 8px 22px rgba(10,30,56,.28);border:1px solid rgba(198,161,91,.55)}.btn-teal:hover{background:#0E2748;transform:translateY(-2px)}
.btn-dark{background:var(--navy);color:#fff}.btn-dark:hover{background:#0a1c37;transform:translateY(-2px)}
header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.85);backdrop-filter:saturate(160%) blur(12px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:1.3rem;color:var(--navy)}.brand .go{color:var(--teal)}.brand svg{width:32px;height:32px;flex:none}
.menu{display:flex;align-items:center;gap:22px}.menu a.link{font-weight:500;color:#33475b;font-size:.94rem}.menu a.link:hover{color:var(--teal-d)}
.right{display:flex;align-items:center;gap:12px}.langs{display:flex;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:3px}
.langs a{font-weight:600;font-size:.78rem;color:var(--muted);padding:5px 9px;border-radius:999px}.langs a.active{background:var(--navy);color:#fff}
.burger{display:none;background:none;border:0;cursor:pointer}.burger svg{width:28px;height:28px;color:var(--navy)}
.hero{position:relative;color:#fff;background:radial-gradient(1100px 480px at 82% -12%,rgba(198,161,91,.28),transparent 60%),linear-gradient(135deg,#081629 0%,#0C2444 55%,#12345E 100%);overflow:hidden}
.hero:after{content:"";position:absolute;right:-120px;bottom:-140px;width:420px;height:420px;background:radial-gradient(circle,rgba(198,161,91,.26),transparent 65%);filter:blur(20px)}
.hero .wrap{position:relative;z-index:2}
.crumb{font-size:.85rem;color:#a9c1dd;padding-top:22px}.crumb a{color:#cfe0f2}.crumb a:hover{color:#fff}
.hero h1{font-size:2.7rem;font-weight:800;margin:14px 0 14px;max-width:820px}
.hero p.sub{font-size:1.12rem;color:#d7e3f2;max-width:640px}.hero-cta{display:flex;gap:12px;margin-top:22px;flex-wrap:wrap}
.homehero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center;padding:56px 22px 70px}
.homehero h1{font-size:3.1rem}.stars{display:flex;align-items:center;gap:10px;margin-top:22px;color:#cfe0f2;font-size:.92rem}.stars .s{color:var(--amber);letter-spacing:2px}
.book{background:#fff;color:var(--ink);border-radius:var(--r-lg);box-shadow:var(--shadow-lg);padding:24px}.book h3{font-size:1.14rem;margin-bottom:4px;color:var(--navy)}.book .muted{color:var(--muted);font-size:.9rem;margin-bottom:14px}
.field{margin-bottom:12px}.field label{display:block;font-size:.76rem;font-weight:600;color:var(--muted);margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em}
.field .in{display:flex;align-items:center;gap:9px;border:1.5px solid var(--line);border-radius:12px;padding:11px 13px;background:var(--soft)}.field .in:focus-within{border-color:var(--teal);background:#fff}
.field .in svg{width:17px;height:17px;color:var(--teal-d);flex:none}.field input,.field select,.field textarea{border:0;background:transparent;font:inherit;color:var(--ink);width:100%;outline:none}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.book .btn{width:100%;justify-content:center;margin-top:6px}
.trust{background:var(--navy);color:#cfe0f2}.trust .wrap{display:flex;flex-wrap:wrap;justify-content:center;gap:12px 34px;padding:18px 22px;text-align:center;font-weight:500;font-size:.92rem}.trust b{color:#fff}.trust .dot{color:var(--teal)}
.sec-head{max-width:680px;margin:0 auto 42px;text-align:center}.sec-head h2{font-size:2.1rem;font-weight:800;color:var(--navy);margin:12px 0 10px}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px 20px;transition:.22s;display:block}
.card:hover{transform:translateY(-6px);box-shadow:var(--shadow);border-color:transparent}.ic{width:50px;height:50px;border-radius:14px;display:grid;place-items:center;margin-bottom:14px;background:var(--mint)}.ic svg{width:25px;height:25px;color:var(--teal-d)}
.card h3{font-size:1.08rem;color:var(--navy);margin-bottom:7px}.card p{font-size:.93rem;color:var(--muted)}.card .more{display:inline-block;margin-top:10px;color:var(--teal-d);font-weight:600;font-size:.9rem}
.article{padding:52px 0}.article .wrap{display:grid;grid-template-columns:1fr;gap:8px;max-width:860px}
.article h2{font-size:1.6rem;color:var(--navy);margin:26px 0 10px}.article p{margin-bottom:12px;color:#33475b}.article ul{margin:6px 0 16px;padding-left:4px;list-style:none}
.article li{position:relative;padding-left:28px;margin-bottom:9px;color:#33475b}.article li:before{content:"";position:absolute;left:0;top:9px;width:16px;height:16px;background:var(--mint);border-radius:50%}
.article li:after{content:"";position:absolute;left:5px;top:12px;width:6px;height:3px;border-left:2px solid var(--teal-d);border-bottom:2px solid var(--teal-d);transform:rotate(-45deg)}
.faq{background:var(--soft)}.faq .wrap{max-width:860px}.qa{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px 22px;margin-bottom:12px}.qa h3{font-size:1.05rem;color:var(--navy);margin-bottom:6px}.qa p{color:var(--muted);font-size:.96rem}
.related{padding:52px 0}.rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.rel{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;font-weight:600;color:var(--navy);display:flex;justify-content:space-between;align-items:center;gap:10px;transition:.2s}.rel:hover{border-color:var(--teal);color:var(--teal-d);transform:translateY(-3px)}
.ctaband{background:linear-gradient(135deg,#0B2545,#1D4E89);color:#fff}.ctaband .wrap{text-align:center;padding:52px 22px}.ctaband h2{font-size:1.9rem;font-weight:800;margin-bottom:8px}.ctaband p{color:#d7e3f2;max-width:560px;margin:0 auto 22px}
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}.chip{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;text-align:center}.chip .n{font-family:'Poppins';font-weight:800;font-size:1.6rem;color:var(--teal-d)}.chip .t{color:var(--muted);font-size:.92rem}
.prices{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.price{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px 20px;text-align:center}.price .t{font-weight:600;color:var(--navy);margin-bottom:6px}.price .n{font-family:'Poppins';font-weight:800;font-size:1.9rem;color:var(--teal-d)}.price .n small{font-size:.78rem;color:var(--muted);font-weight:600}.price .d{font-size:.84rem;color:var(--muted);margin-top:6px}
.form{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px;box-shadow:var(--shadow);max-width:560px}.form .btn{width:100%;justify-content:center}
.cinfo{display:flex;align-items:center;gap:12px;margin-bottom:14px}.cinfo .ci{width:42px;height:42px;border-radius:12px;background:var(--mint);display:grid;place-items:center;flex:none}.cinfo .ci svg{width:19px;height:19px;color:var(--teal-d)}.cinfo b{display:block;font-size:.76rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.05em}
footer{background:#071a30;color:#9fb6d1;padding:48px 0 24px;font-size:.9rem}.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px;margin-bottom:30px}footer .brand{color:#fff;margin-bottom:12px}footer h5{color:#fff;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px}footer a{display:block;margin-bottom:8px;color:#9fb6d1}footer a:hover{color:var(--teal)}
.fbot{border-top:1px solid rgba(255,255,255,.1);padding-top:18px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:.82rem}
.wa{position:fixed;right:20px;bottom:20px;z-index:60;width:58px;height:58px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 10px 26px rgba(37,211,102,.5);transition:.2s}.wa:hover{transform:scale(1.08)}.wa svg{width:31px;height:31px;color:#fff}
@media(max-width:940px){.homehero .wrap{grid-template-columns:1fr;gap:30px}.hero h1,.homehero h1{font-size:2.2rem}.cards,.prices{grid-template-columns:1fr 1fr}.rel-grid,.chips{grid-template-columns:1fr}.fgrid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.menu{display:none}.burger{display:block}.cards,.prices,.fgrid{grid-template-columns:1fr 1fr}section{padding:48px 0}}
"""

# ---------------------------------------------------------------- JS
JS = r"""
(function(){
  var b=document.querySelector('.burger'), m=document.querySelector('.menu');
  if(b&&m)b.addEventListener('click',function(){m.style.display=(getComputedStyle(m).display==='none'?'flex':'none')});
})();
var WA='__WA__';
function waOpen(msg){var t=encodeURIComponent(msg||'Hola BaggageGo, quiero información.');window.open('https://wa.me/'+WA+'?text='+t,'_blank');return false;}
function quote(){
  var g=function(id){var e=document.getElementById(id);return e?e.value:'';};
  waOpen('Hola BaggageGo 🧳\nQuiero precio para una entrega:\n• Recogida: '+(g('f_from')||'—')+'\n• Entrega: '+(g('f_to')||'—')+'\n• Maletas: '+(g('f_bags')||'—')+'\n• Fecha: '+(g('f_date')||'—'));
}
function sendForm(e){e.preventDefault();var g=function(id){var el=document.getElementById(id);return el?el.value:'';};waOpen('Hola BaggageGo, soy '+g('c_name')+' ('+g('c_email')+').\n'+g('c_msg'));}
""".replace("__WA__", WA)

# ---------------------------------------------------------------- HELPERS
def esc(s): return html.escape(s, quote=True)

LOGO = ('<svg viewBox="0 0 100 100"><rect x="24" y="30" width="52" height="46" rx="8" fill="#C6A15B"/>'
        '<rect x="40" y="20" width="20" height="12" rx="4" fill="none" stroke="#0A1E38" stroke-width="5"/>'
        '<circle cx="72" cy="60" r="10" fill="#0A1E38"/></svg>')
WA_ICON = ('<svg fill="currentColor" viewBox="0 0 24 24"><path d="M.06 24l1.68-6.13A11.87 11.87 0 010 5.94 11.94 11.94 0 0112.05 0a11.94 11.94 0 018.4 20.4A11.94 11.94 0 016.2 22.2L.06 24zM6.6 20.13l.37.22a9.86 9.86 0 004.99 1.37 9.9 9.9 0 100-19.8 9.9 9.9 0 00-8.38 15.15l.24.38-1 3.65 3.79-1zM17.5 14.4c-.15-.25-.55-.4-1.15-.7s-1.77-.87-2.04-.97-.47-.15-.67.15-.77.97-.94 1.17-.35.22-.65.07a8.13 8.13 0 01-2.4-1.48 9 9 0 01-1.66-2.06c-.17-.3 0-.46.13-.6s.3-.35.45-.52a2 2 0 00.3-.5.55.55 0 000-.52c-.07-.15-.67-1.62-.92-2.22s-.49-.5-.67-.5h-.57a1.1 1.1 0 00-.8.37 3.35 3.35 0 00-1.04 2.48 5.8 5.8 0 001.22 3.09 13.3 13.3 0 005.1 4.5c.71.3 1.27.49 1.7.63a4.1 4.1 0 001.88.12 3.07 3.07 0 002-1.42 2.5 2.5 0 00.17-1.42z"/></svg>')

# Registro global de todas las paginas para hreflang / sitemap
# entry: {"group":id,"lang":l,"path":relpath_from_root,"prio":float}
REGISTRY = []

def register(group, lang, path, prio=0.6):
    for e in REGISTRY:
        if e["group"]==group and e["lang"]==lang:
            return
    REGISTRY.append({"group":group,"lang":lang,"path":path,"prio":prio})

def plan():
    """Registra TODAS las rutas antes de generar, para hreflang correcto."""
    for lang in LANGS:
        register("home", lang, LANG_BASE[lang]+"index.html", 1.0)
        for s in SERVICES:
            register("serv_"+s["id"], lang, LANG_BASE[lang]+SEG[lang]["serv"]+"/"+s["slug"][lang]+".html", 0.8)
        for z in ZONES:
            register("zona_"+z["id"], lang, LANG_BASE[lang]+SEG[lang]["zona"]+"/"+z["slug"]+".html", 0.7)
        for key in INFO_SLUG:
            register("info_"+key, lang, LANG_BASE[lang]+INFO_SLUG[key][lang]+".html", 0.6)
        for a in BLOG:
            register("blog_"+a["id"], lang, LANG_BASE[lang]+SEG_BLOG[lang]+"/"+a["slug"][lang]+".html", 0.5)

def url_abs(path):
    return DOMAIN + "/" + path if path else DOMAIN + "/"

def rel(from_path, to_path):
    """URL relativa (para file:// y hosting) de from_path a to_path."""
    fd = os.path.dirname(from_path)
    r = os.path.relpath(to_path, fd if fd else ".")
    return r.replace("\\", "/")

def group_paths(group):
    """dict lang->path para un grupo (para hreflang y selector idioma)."""
    d = {}
    for e in REGISTRY:
        if e["group"] == group:
            d[e["lang"]] = e["path"]
    return d

# ---------------------------------------------------------------- LAYOUT
def head(lang, title, desc, out_path, group, jsonld_list):
    gp = group_paths(group)
    alts = ""
    for l in LANGS:
        if l in gp:
            alts += '<link rel="alternate" hreflang="%s" href="%s">\n' % (l, url_abs(gp[l]))
    if "es" in gp:
        alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % url_abs(gp["es"])
    css_href = rel(out_path, "styles.css")
    canonical = url_abs(out_path)
    og_locale = {"es":"es_ES","en":"en_GB","de":"de_DE"}[lang]
    jsonld = "\n".join('<script type="application/ld+json">%s</script>' % j for j in jsonld_list)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{alts}<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND} Mallorca">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect x='24' y='30' width='52' height='46' rx='8' fill='%23C6A15B'/><rect x='40' y='20' width='20' height='12' rx='4' fill='none' stroke='%230A1E38' stroke-width='5'/><circle cx='72' cy='60' r='10' fill='%230A1E38'/></svg>">
<link rel="stylesheet" href="{css_href}">
{jsonld}
</head>
<body>
"""

def header(lang, out_path, group):
    ui = UI[lang]
    home = LANG_BASE[lang] + "index.html"
    # nav: servicios/zonas apuntan al home con ancla; info a sus paginas
    items = ""
    for label, tgt in ui["nav"]:
        if tgt.startswith("#"):
            href = rel(out_path, home) + tgt
        else:
            slug = INFO_SLUG.get(_info_key_by_slug(tgt, lang), {}).get(lang, tgt)
            href = rel(out_path, LANG_BASE[lang] + slug + ".html")
        items += f'<a class="link" href="{href}">{esc(label)}</a>'
    # selector de idioma -> equivalente de la misma pagina
    gp = group_paths(group)
    langs_html = ""
    for l in LANGS:
        cls = "active" if l == lang else ""
        target = gp.get(l, LANG_BASE[l] + "index.html")
        langs_html += f'<a class="{cls}" href="{rel(out_path, target)}">{l.upper()}</a>'
    contact_slug = INFO_SLUG["contacto"][lang]
    book_href = rel(out_path, LANG_BASE[lang] + contact_slug + ".html")
    return f"""<header><div class="wrap nav">
<a href="{rel(out_path, home)}" class="brand">{LOGO} Baggage<span class="go">Go</span></a>
<nav class="menu">{items}</nav>
<div class="right">
<div class="langs">{langs_html}</div>
<a href="{book_href}" class="btn btn-primary" style="padding:10px 18px">{esc(ui['book'])}</a>
<button class="burger" aria-label="menu"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
</div></div></header>"""

def _info_key_by_slug(slug, lang):
    for k, v in INFO_SLUG.items():
        if v[lang] == slug or k == slug:
            return k
    return slug

def footer(lang, out_path):
    ui = UI[lang]
    home = LANG_BASE[lang] + "index.html"
    def sv(sid):
        s = next(x for x in SERVICES if x["id"]==sid)
        return rel(out_path, LANG_BASE[lang] + SEG[lang]["serv"] + "/" + s["slug"][lang] + ".html")
    def info(key):
        return rel(out_path, LANG_BASE[lang] + INFO_SLUG[key][lang] + ".html")
    labels = {
      "es":{"serv":"Servicios","comp":"Empresa","cont":"Contacto","s":["Entrega de maletas","Consigna","Ciclistas y senderistas","BaggageGo Moving"],"c":["Cómo funciona","Precios","Para hoteles","Contacto"]},
      "en":{"serv":"Services","comp":"Company","cont":"Contact","s":["Luggage delivery","Storage","Cyclists & hikers","BaggageGo Moving"],"c":["How it works","Prices","For hotels","Contact"]},
      "de":{"serv":"Leistungen","comp":"Unternehmen","cont":"Kontakt","s":["Gepäcklieferung","Aufbewahrung","Radfahrer & Wanderer","BaggageGo Moving"],"c":["Ablauf","Preise","Für Hotels","Kontakt"]},
    }[lang]
    return f"""<footer><div class="wrap">
<div class="fgrid">
<div><div class="brand" style="font-size:1.2rem">Baggage<span style="color:var(--teal)">Go</span></div>
<p>{esc(ui['foot_tag'])}</p><p style="margin-top:10px;font-size:.82rem;color:#6f88a6">{esc(ui['foot_company'])}</p></div>
<div><h5>{esc(labels['serv'])}</h5>
<a href="{sv('aeropuerto')}">{esc(labels['s'][0])}</a><a href="{sv('consigna')}">{esc(labels['s'][1])}</a>
<a href="{sv('ciclistas')}">{esc(labels['s'][2])}</a><a href="{sv('mudanzas')}">{esc(labels['s'][3])}</a></div>
<div><h5>{esc(labels['comp'])}</h5>
<a href="{info('como-funciona')}">{esc(labels['c'][0])}</a><a href="{info('precios')}">{esc(labels['c'][1])}</a>
<a href="{info('hoteles-y-partners')}">{esc(labels['c'][2])}</a><a href="{info('contacto')}">{esc(labels['c'][3])}</a></div>
<div><h5>{esc(labels['cont'])}</h5><a href="https://wa.me/{WA}">{esc(PHONE_DISPLAY)}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a>{esc(CITY)}</a></div>
</div>
<div class="fbot"><span>© 2026 {BRAND} Mallorca</span><span>{esc(ui['draft'])}</span></div>
</div></footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_ICON}</a>
<script src="{rel(out_path,'main.js')}"></script>
</body></html>"""

def breadcrumb(lang, out_path, trail):
    # trail: list of (label, path_or_None)
    parts = []
    for label, p in trail:
        if p:
            parts.append(f'<a href="{rel(out_path,p)}">{esc(label)}</a>')
        else:
            parts.append(esc(label))
    return '<div class="wrap crumb">' + " › ".join(parts) + '</div>'

def jsonld_breadcrumb(trail_abs):
    items = ",".join(
        '{"@type":"ListItem","position":%d,"name":%s,"item":"%s"}' % (i+1, _json(name), url)
        for i,(name,url) in enumerate(trail_abs))
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}' % items

def jsonld_faq(faq):
    q = ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (_json(a),_json(b)) for a,b in faq)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % q

def jsonld_localbusiness():
    return ('{"@context":"https://schema.org","@type":"MovingCompany","name":"%s Mallorca",'
            '"description":"Entrega de equipaje y mudanzas en Mallorca","areaServed":"Mallorca",'
            '"url":"%s","telephone":"%s","email":"%s","address":{"@type":"PostalAddress","addressLocality":"%s","addressRegion":"Illes Balears","addressCountry":"ES"}}'
            % (BRAND, DOMAIN, PHONE_DISPLAY, EMAIL, CITY))

def _json(s):
    return '"' + s.replace("\\","\\\\").replace('"','\\"').replace("\n"," ") + '"'

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- CTA band
def cta_band(lang, out_path):
    ui = UI[lang]
    contact = rel(out_path, LANG_BASE[lang] + INFO_SLUG["contacto"][lang] + ".html")
    return f"""<section class="ctaband"><div class="wrap">
<h2>{esc(ui['cta_band_t'])}</h2><p>{esc(ui['cta_band_p'])}</p>
<a href="{contact}" class="btn btn-primary">{esc(ui['cta_main'])}</a>
</div></section>"""

# related services block
def related_services(lang, out_path, exclude=None):
    ui = UI[lang]
    names = {"es":{"aeropuerto":"Entrega desde el aeropuerto","consigna":"Consigna de equipaje","ciclistas":"Equipaje para ciclistas","mudanzas":"Mudanzas exprés","mercancias":"Transporte de mercancías","guardamuebles":"Guardamuebles","bicicletas":"Transporte de bicicletas"},
             "en":{"aeropuerto":"Airport delivery","consigna":"Luggage storage","ciclistas":"Cyclist luggage","mudanzas":"Express moving","mercancias":"Cargo van & goods","guardamuebles":"Storage","bicicletas":"Bike transport"},
             "de":{"aeropuerto":"Flughafen-Lieferung","consigna":"Gepäckaufbewahrung","ciclistas":"Radfahrer-Gepäck","mudanzas":"Express-Umzüge","mercancias":"Warentransport","guardamuebles":"Einlagerung","bicicletas":"Fahrradtransport"}}[lang]
    cards = ""
    for s in SERVICES:
        if s["id"]==exclude: continue
        href = rel(out_path, LANG_BASE[lang]+SEG[lang]["serv"]+"/"+s["slug"][lang]+".html")
        cards += f'<a class="rel" href="{href}">{esc(names[s["id"]])} <span class="accent">→</span></a>'
    return f'<section class="related"><div class="wrap"><div class="sec-head"><h2>{esc(ui["related_s"])}</h2></div><div class="rel-grid">{cards}</div></div></section>'

def related_zones(lang, out_path):
    ui = UI[lang]
    cards = ""
    for z in ZONES:
        href = rel(out_path, LANG_BASE[lang]+SEG[lang]["zona"]+"/"+z["slug"]+".html")
        cards += f'<a class="rel" href="{href}">{esc(z["name"])} <span class="accent">→</span></a>'
    return f'<section class="related" style="background:var(--soft)"><div class="wrap"><div class="sec-head"><h2>{esc(ui["related_z"])}</h2></div><div class="rel-grid">{cards}</div></div></section>'

# ---------------------------------------------------------------- PAGE BUILDERS
def build_service(s, lang):
    out = LANG_BASE[lang] + SEG[lang]["serv"] + "/" + s["slug"][lang] + ".html"
    group = "serv_" + s["id"]
    ui = UI[lang]
    home = LANG_BASE[lang]+"index.html"
    trail = [(ui["home"], home), (ui["services_t"], home+"#servicios"), (s["h1"][lang], None)]
    trail_abs = [(ui["home"], url_abs(home)), (s["h1"][lang], url_abs(out))]
    jl = [jsonld_localbusiness(), jsonld_breadcrumb(trail_abs), jsonld_faq(s["faq"][lang]),
          '{"@context":"https://schema.org","@type":"Service","serviceType":%s,"provider":{"@type":"Organization","name":"%s Mallorca"},"areaServed":"Mallorca","description":%s}' % (_json(s["h1"][lang]), BRAND, _json(s["desc"][lang]))]
    H = head(lang, s["title"][lang], s["desc"][lang], out, group, jl)
    hero = f"""<section class="hero">{breadcrumb(lang,out,trail)}
<div class="wrap"><h1>{esc(s['h1'][lang])}</h1><p class="sub">{esc(s['intro'][lang])}</p>
<div class="hero-cta"><a href="{rel(out,LANG_BASE[lang]+INFO_SLUG['contacto'][lang]+'.html')}" class="btn btn-primary">{esc(ui['cta_main'])}</a>
<a href="https://wa.me/{WA}" class="btn btn-ghost" target="_blank" rel="noopener">{esc(ui['wa'])}</a></div>
<div style="height:26px"></div></div></section>"""
    body = '<section class="article"><div class="wrap">'
    for h2, p, li in s["secs"][lang]:
        body += f"<h2>{esc(h2)}</h2><p>{esc(p)}</p>"
        if li:
            body += "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in li) + "</ul>"
    body += "</div></section>"
    faq = f'<section class="faq"><div class="wrap"><div class="sec-head"><span class="eyebrow">FAQ</span><h2>{esc(ui["faq"])}</h2></div>'
    for q,a in s["faq"][lang]:
        faq += f'<div class="qa"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>'
    faq += "</div></section>"
    page = H + header(lang,out,group) + hero + body + faq + related_services(lang,out,exclude=s["id"]) + related_zones(lang,out) + cta_band(lang,out) + footer(lang,out)
    write(out, page)
    register(group, lang, out, 0.8)

def zone_faq(lang, name):
    return {
     "es":[("¿Cuánto cuesta la entrega de maletas en "+name+"?","Desde 10 € por dos maletas puerta a puerta en "+name+". El precio depende del número de bultos y del punto exacto; te lo confirmamos al instante por WhatsApp."),
           ("¿Entregáis en "+name+" el mismo día?","Sí. Con reserva anticipada entregamos tu equipaje en "+name+" el mismo día, y también lo recogemos para llevarlo al aeropuerto o a otro alojamiento.")],
     "en":[("How much is luggage delivery in "+name+"?","From €10 for two bags door to door in "+name+". The price depends on the number of items and the exact point; we confirm instantly on WhatsApp."),
           ("Do you deliver in "+name+" the same day?","Yes. With advance booking we deliver your luggage in "+name+" the same day, and we also collect it to take to the airport or another accommodation.")],
     "de":[("Was kostet die Gepäcklieferung in "+name+"?","Ab 10 € für zwei Gepäckstücke von Tür zu Tür in "+name+". Der Preis hängt von der Anzahl der Stücke und dem genauen Ort ab; wir bestätigen sofort per WhatsApp."),
           ("Liefert ihr in "+name+" am selben Tag?","Ja. Bei rechtzeitiger Buchung liefern wir dein Gepäck in "+name+" am selben Tag und holen es auch ab, um es zum Flughafen oder zu einer anderen Unterkunft zu bringen.")],
    }[lang]

def build_zone(z, lang):
    out = LANG_BASE[lang] + SEG[lang]["zona"] + "/" + z["slug"] + ".html"
    group = "zona_" + z["id"]
    ui = UI[lang]
    zd = z[lang]
    home = LANG_BASE[lang]+"index.html"
    trail = [(ui["home"], home), (ui["zones_t"], home+"#zonas"), (z["name"], None)]
    trail_abs = [(ui["home"], url_abs(home)), (zd["h1"], url_abs(out))]
    faqs = zone_faq(lang, z["name"])
    jl = [jsonld_localbusiness(), jsonld_breadcrumb(trail_abs), jsonld_faq(faqs),
          '{"@context":"https://schema.org","@type":"Service","serviceType":%s,"provider":{"@type":"Organization","name":"%s Mallorca"},"areaServed":%s,"description":%s}' % (_json(zd["h1"]), BRAND, _json(z["name"]+", Mallorca"), _json(zd["desc"]))]
    H = head(lang, zd["title"], zd["desc"], out, group, jl)
    hero = f"""<section class="hero">{breadcrumb(lang,out,trail)}
<div class="wrap"><h1>{esc(zd['h1'])}</h1><p class="sub">{esc(zd['intro'])}</p>
<div class="hero-cta"><a href="{rel(out,LANG_BASE[lang]+INFO_SLUG['contacto'][lang]+'.html')}" class="btn btn-primary">{esc(ui['cta_main'])}</a>
<a href="https://wa.me/{WA}" class="btn btn-ghost" target="_blank" rel="noopener">{esc(ui['wa'])}</a></div><div style="height:26px"></div></div></section>"""
    svz = lambda sid: rel(out, LANG_BASE[lang]+SEG[lang]["serv"]+"/"+next(x for x in SERVICES if x["id"]==sid)["slug"][lang]+".html")
    h2z = {"es":"Servicios de BaggageGo en "+z["name"],"en":"BaggageGo services in "+z["name"],"de":"BaggageGo-Leistungen in "+z["name"]}[lang]
    paraz = {
     "es":'En %s ofrecemos <a href="%s">entrega de maletas</a>, <a href="%s">consigna de equipaje</a>, <a href="%s">transporte de bicicletas</a> y <a href="%s">mudanzas exprés</a>. Recogemos en el aeropuerto, tu hotel o tu villa y entregamos donde lo necesites, con seguro y seguimiento.' % (z["name"], svz("aeropuerto"), svz("consigna"), svz("bicicletas"), svz("mudanzas")),
     "en":'In %s we offer <a href="%s">luggage delivery</a>, <a href="%s">luggage storage</a>, <a href="%s">bike transport</a> and <a href="%s">express moving</a>. We collect at the airport, your hotel or your villa and deliver wherever you need, insured and tracked.' % (z["name"], svz("aeropuerto"), svz("consigna"), svz("bicicletas"), svz("mudanzas")),
     "de":'In %s bieten wir <a href="%s">Gepäcklieferung</a>, <a href="%s">Gepäckaufbewahrung</a>, <a href="%s">Fahrradtransport</a> und <a href="%s">Express-Umzüge</a>. Wir holen am Flughafen, in deinem Hotel oder deiner Villa ab und liefern, wohin du willst, versichert und verfolgt.' % (z["name"], svz("aeropuerto"), svz("consigna"), svz("bicicletas"), svz("mudanzas")),
    }[lang]
    body = '<section class="article"><div class="wrap"><h2>'+esc(h2z)+'</h2><p>'+paraz+'</p><ul>'
    body += "".join(f"<li>{esc(x)}</li>" for x in zd["hi"])
    body += "</ul></div></section>"
    faq_html = '<section class="faq"><div class="wrap"><div class="sec-head"><span class="eyebrow">FAQ</span><h2>'+esc(ui["faq"])+'</h2></div>'
    for q,a in faqs:
        faq_html += '<div class="qa"><h3>'+esc(q)+'</h3><p>'+esc(a)+'</p></div>'
    faq_html += "</div></section>"
    page = H + header(lang,out,group) + hero + body + faq_html + related_services(lang,out) + related_zones(lang,out) + cta_band(lang,out) + footer(lang,out)
    write(out, page)
    register(group, lang, out, 0.7)

def build_info(key, lang, title, desc, h1, blocks, extra=""):
    out = LANG_BASE[lang] + INFO_SLUG[key][lang] + ".html"
    group = "info_" + key
    ui = UI[lang]
    home = LANG_BASE[lang]+"index.html"
    trail=[(ui["home"],home),(h1,None)]
    trail_abs=[(ui["home"],url_abs(home)),(h1,url_abs(out))]
    jl=[jsonld_localbusiness(), jsonld_breadcrumb(trail_abs)]
    H=head(lang,title,desc,out,group,jl)
    hero=f"""<section class="hero">{breadcrumb(lang,out,trail)}<div class="wrap"><h1>{esc(h1)}</h1><p class="sub">{esc(desc)}</p><div style="height:26px"></div></div></section>"""
    page=H+header(lang,out,group)+hero+blocks+extra+cta_band(lang,out)+footer(lang,out)
    write(out,page)
    register(group,lang,out,0.6)

# ---------------------------------------------------------------- HOME
def build_home(lang):
    out = LANG_BASE[lang] + "index.html"
    group = "home"
    ui = UI[lang]
    T={"es":{"title":"BaggageGo Mallorca · Entrega de maletas y mudanzas","desc":"Entrega de maletas puerta a puerta en Mallorca: aeropuerto, hoteles y villas. Servicio para ciclistas de la Tramuntana, consigna y mudanzas exprés. ES·EN·DE.",
             "eyebrow":"Entrega de equipaje y mudanzas en Mallorca","h1a":"Tus maletas","h1b":"viajan solas.",
             "sub":"Recogemos tu equipaje en el aeropuerto, hotel o villa y lo entregamos donde tú estés. Tú viaja ligero.",
             "book_t":"Calcula tu precio","book_p":"Equipaje de un punto a otro, en toda la isla.","f_from":"Recogida","f_to":"Entrega","f_bags":"Maletas","f_date":"Fecha",
             "sh_s_e":"Nuestros servicios","sh_s_t":"Todo se mueve, para que tú no cargues nada","sh_z_e":"SEO local","sh_z_t":"Entrega de maletas por zonas de Mallorca",
             "svc":{"aeropuerto":("Maletas puerta a puerta","Aeropuerto ↔ hotel ↔ villa. Llega con las manos libres."),"consigna":("Consigna de equipaje","Guarda tus maletas por horas antes del check-in o después del check-out."),"ciclistas":("Ciclistas y senderistas","Movemos tu equipaje y tu bici de hotel a hotel por la Tramuntana."),"mudanzas":("BaggageGo Moving","Mudanzas pequeñas y exprés en la isla: rápidas y aseguradas."),"mercancias":("Transporte de mercancías","Furgoneta con conductor para mercancía y envíos voluminosos en toda la isla."),"guardamuebles":("Guardamuebles","Almacenaje seguro por meses, con recogida y entrega a domicilio."),"bicicletas":("Transporte de bicicletas","Del aeropuerto al hotel y entre etapas, para cicloturistas y grupos.")},
             "more":"Ver más","ver_zona":"Ver zona"},
       "en":{"title":"BaggageGo Mallorca · Luggage delivery & moving","desc":"Door-to-door luggage delivery in Mallorca: airport, hotels and villas. Service for Tramuntana cyclists, storage and express moving. ES·EN·DE.",
             "eyebrow":"Luggage delivery & moving in Mallorca","h1a":"Your bags","h1b":"travel on their own.",
             "sub":"We pick up your luggage at the airport, hotel or villa and deliver it wherever you are. You just travel light.",
             "book_t":"Get an instant price","book_p":"Luggage from A to B, anywhere on the island.","f_from":"From","f_to":"To","f_bags":"Bags","f_date":"Date",
             "sh_s_e":"What we do","sh_s_t":"Everything moves, so you don't have to","sh_z_e":"Local SEO","sh_z_t":"Luggage delivery by area in Mallorca",
             "svc":{"aeropuerto":("Door-to-door luggage","Airport ↔ hotel ↔ villa. Arrive hands-free."),"consigna":("Luggage storage","Store your bags by the hour before check-in or after check-out."),"ciclistas":("Cyclists & hikers","We move your luggage and bike hotel to hotel across the Tramuntana."),"mudanzas":("BaggageGo Moving","Small, express moves across the island: fast and insured."),"mercancias":("Cargo van & goods","A cargo van with driver for goods and bulky deliveries island-wide."),"guardamuebles":("Storage","Secure monthly storage, with home pick-up and delivery."),"bicicletas":("Bike transport","From airport to hotel and between stages, for cyclists and groups.")},
             "more":"Learn more","ver_zona":"View area"},
       "de":{"title":"BaggageGo Mallorca · Gepäcklieferung & Umzüge","desc":"Gepäcklieferung von Tür zu Tür auf Mallorca: Flughafen, Hotels und Villen. Service für Tramuntana-Radfahrer, Aufbewahrung und Express-Umzüge. ES·EN·DE.",
             "eyebrow":"Gepäcklieferung & Umzüge auf Mallorca","h1a":"Dein Gepäck","h1b":"reist von allein.",
             "sub":"Wir holen dein Gepäck am Flughafen, Hotel oder in der Villa ab und liefern es dorthin, wo du bist. Reise einfach leicht.",
             "book_t":"Sofortpreis erhalten","book_p":"Gepäck von A nach B, überall auf der Insel.","f_from":"Von","f_to":"Nach","f_bags":"Gepäck","f_date":"Datum",
             "sh_s_e":"Was wir tun","sh_s_t":"Alles bewegt sich – nur du nicht","sh_z_e":"Lokales SEO","sh_z_t":"Gepäcklieferung nach Gebiet auf Mallorca",
             "svc":{"aeropuerto":("Gepäck von Tür zu Tür","Flughafen ↔ Hotel ↔ Villa. Komm mit freien Händen an."),"consigna":("Gepäckaufbewahrung","Lagere dein Gepäck stundenweise vor dem Check-in oder nach dem Check-out."),"ciclistas":("Radfahrer & Wanderer","Wir bringen dein Gepäck und dein Rad von Hotel zu Hotel durch die Tramuntana."),"mudanzas":("BaggageGo Moving","Kleine Express-Umzüge auf der Insel: schnell und versichert."),"mercancias":("Warentransport","Transporter mit Fahrer für Waren und sperrige Lieferungen inselweit."),"guardamuebles":("Einlagerung","Sichere monatliche Einlagerung, mit Abholung und Lieferung."),"bicicletas":("Fahrradtransport","Vom Flughafen zum Hotel und zwischen Etappen, für Radfahrer und Gruppen.")},
             "more":"Mehr erfahren","ver_zona":"Gebiet ansehen"}}[lang]
    jl=[jsonld_localbusiness(),
        '{"@context":"https://schema.org","@type":"WebSite","name":"%s Mallorca","url":"%s"}' % (BRAND, url_abs(out))]
    H=head(lang,T["title"],T["desc"],out,group,jl)
    contact=rel(out,LANG_BASE[lang]+INFO_SLUG["contacto"][lang]+".html")
    # hero + booking
    hero=f"""<section class="hero homehero"><div class="wrap">
<div><span class="eyebrow" style="background:rgba(198,161,91,.16);color:#E7D4A3">{esc(T['eyebrow'])}</span>
<h1>{esc(T['h1a'])} <span class="accent">{esc(T['h1b'])}</span></h1>
<p class="sub">{esc(T['sub'])}</p>
<div class="hero-cta"><a href="{contact}" class="btn btn-primary">{esc(ui['cta_main'])}</a>
<a href="{rel(out,LANG_BASE[lang]+SEG[lang]['serv']+'/'+[s for s in SERVICES if s['id']=='mudanzas'][0]['slug'][lang]+'.html')}" class="btn btn-ghost">{esc(ui['hero_cta2'])}</a></div>
<div class="stars"><span class="s">★★★★★</span> {esc(ui['insured'])} · ES · EN · DE</div></div>
<div class="book"><h3>{esc(T['book_t'])}</h3><p class="muted">{esc(T['book_p'])}</p>
<div class="field"><label>{esc(T['f_from'])}</label><div class="in"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 21s-7-6.4-7-11a7 7 0 0114 0c0 4.6-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><input id="f_from" placeholder="PMI, hotel…"></div></div>
<div class="field"><label>{esc(T['f_to'])}</label><div class="in"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 21s-7-6.4-7-11a7 7 0 0114 0c0 4.6-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><input id="f_to" placeholder="Hotel, villa…"></div></div>
<div class="grid2"><div class="field"><label>{esc(T['f_bags'])}</label><div class="in"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="5" y="8" width="14" height="12" rx="2"/><path d="M9 8V5h6v3"/></svg><select id="f_bags"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div></div>
<div class="field"><label>{esc(T['f_date'])}</label><div class="in"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 9h16M8 3v4M16 3v4"/></svg><input id="f_date" type="date"></div></div></div>
<button class="btn btn-teal" onclick="quote()">{esc(ui['wa'])}</button></div>
</div></section>"""
    trust=f"""<div class="trust"><div class="wrap"><span><b>2,4M</b> pax/mes PMI</span><span class="dot">●</span><span><b>Hoteles & Villas</b></span><span class="dot">●</span><span><b>Serra de Tramuntana</b></span><span class="dot">●</span><span><b>{esc(ui['insured'])}</b></span></div></div>"""
    # servicios
    scards=""
    for s in SERVICES:
        nm,ds=T["svc"][s["id"]]
        href=rel(out,LANG_BASE[lang]+SEG[lang]["serv"]+"/"+s["slug"][lang]+".html")
        scards+=f'<a class="card" href="{href}"><div class="ic"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">{s["icon"]}</svg></div><h3>{esc(nm)}</h3><p>{esc(ds)}</p><span class="more">{esc(T["more"])} →</span></a>'
    servicios=f'<section id="servicios"><div class="wrap"><div class="sec-head"><span class="eyebrow">{esc(T["sh_s_e"])}</span><h2>{esc(T["sh_s_t"])}</h2></div><div class="cards">{scards}</div></div></section>'
    # zonas
    zcards=""
    for z in ZONES:
        href=rel(out,LANG_BASE[lang]+SEG[lang]["zona"]+"/"+z["slug"]+".html")
        zcards+=f'<a class="rel" href="{href}">{esc(z["name"])} <span class="accent">→</span></a>'
    zonas=f'<section id="zonas" style="background:var(--soft)"><div class="wrap"><div class="sec-head"><span class="eyebrow">{esc(T["sh_z_e"])}</span><h2>{esc(T["sh_z_t"])}</h2></div><div class="rel-grid">{zcards}</div></div></section>'
    page=H+header(lang,out,group)+hero+trust+servicios+zonas+cta_band(lang,out)+footer(lang,out)
    write(out,page)
    register(group,lang,out,1.0)

# ---------------------------------------------------------------- INFO CONTENT
def build_info_pages(lang):
    ui=UI[lang]
    # Cómo funciona
    steps={"es":[("Reserva online","Dinos recogida, entrega y hora. En 2 minutos por la web o WhatsApp."),("Recogemos","Nuestro conductor recoge tu equipaje en el punto acordado."),("Entregamos","Puntual y asegurado, con seguimiento de principio a fin.")],
           "en":[("Book online","Tell us pick-up, drop-off and time. 2 minutes via web or WhatsApp."),("We pick up","Our driver collects your luggage at the agreed point."),("We deliver","On time and insured, with tracking end to end.")],
           "de":[("Online buchen","Sag uns Abholung, Ziel und Uhrzeit. In 2 Minuten per Web oder WhatsApp."),("Wir holen ab","Unser Fahrer holt dein Gepäck am vereinbarten Ort ab."),("Wir liefern","Pünktlich und versichert, mit Sendungsverfolgung.")]}[lang]
    cf_title={"es":"Cómo funciona · BaggageGo Mallorca","en":"How it works · BaggageGo Mallorca","de":"So funktioniert es · BaggageGo Mallorca"}[lang]
    cf_h1={"es":"Cómo funciona BaggageGo","en":"How BaggageGo works","de":"So funktioniert BaggageGo"}[lang]
    cf_desc={"es":"Reserva, recogemos y entregamos tu equipaje en Mallorca. Tres pasos, asegurado y con seguimiento.","en":"Book, we pick up and we deliver your luggage in Mallorca. Three steps, insured and tracked.","de":"Buchen, wir holen ab und liefern dein Gepäck auf Mallorca. Drei Schritte, versichert und verfolgbar."}[lang]
    blocks='<section class="article"><div class="wrap">'
    for i,(h,p) in enumerate(steps,1):
        blocks+=f"<h2>{i}. {esc(h)}</h2><p>{esc(p)}</p>"
    blocks+="</div></section>"
    build_info("como-funciona",lang,cf_title,cf_desc,cf_h1,blocks,related_services(lang,LANG_BASE[lang]+INFO_SLUG['como-funciona'][lang]+'.html'))

    # Precios
    pr={"es":[("Entrega de maletas","10€","2 maletas, puerta a puerta"),("Bicicletas","18€","por bici / día"),("Consigna","5€","por maleta / día"),("BaggageGo Moving","300€","presupuesto a medida")],
        "en":[("Luggage delivery","10€","2 bags, door to door"),("Bicycles","18€","per bike / day"),("Storage","5€","per bag / day"),("BaggageGo Moving","300€","custom quote")],
        "de":[("Gepäcklieferung","10€","2 Stück, Tür zu Tür"),("Fahrräder","18€","pro Rad / Tag"),("Aufbewahrung","5€","pro Stück / Tag"),("BaggageGo Moving","300€","individuelles Angebot")]}[lang]
    pr_title={"es":"Precios · BaggageGo Mallorca","en":"Prices · BaggageGo Mallorca","de":"Preise · BaggageGo Mallorca"}[lang]
    pr_h1={"es":"Precios orientativos","en":"Indicative prices","de":"Richtpreise"}[lang]
    pr_desc={"es":"Tarifas de referencia de entrega de maletas, consigna, bicicletas y mudanzas exprés en Mallorca.","en":"Reference rates for luggage delivery, storage, bikes and express moving in Mallorca.","de":"Richtpreise für Gepäcklieferung, Aufbewahrung, Fahrräder und Express-Umzüge auf Mallorca."}[lang]
    note={"es":"* Precios de referencia, junio 2026. No constituyen oferta vinculante.","en":"* Reference prices, June 2026. Not a binding offer.","de":"* Richtpreise, Juni 2026. Kein verbindliches Angebot."}[lang]
    cards="".join(f'<div class="price"><div class="t">{esc(t)}</div><div class="n"><small>{esc(ui["price_from"])}</small> {esc(n)}</div><div class="d">{esc(d)}</div></div>' for t,n,d in pr)
    blocks=f'<section><div class="wrap"><div class="prices">{cards}</div><p class="center" style="color:var(--muted);font-size:.85rem;margin-top:20px">{esc(note)}</p></div></section>'
    build_info("precios",lang,pr_title,pr_desc,pr_h1,blocks)

    # Hoteles / partners
    ht_title={"es":"Para hoteles, villas e inmobiliarias · BaggageGo","en":"For hotels, villas & real estate · BaggageGo","de":"Für Hotels, Villen & Immobilien · BaggageGo"}[lang]
    ht_h1={"es":"Hazte partner de BaggageGo","en":"Become a BaggageGo partner","de":"Werde BaggageGo-Partner"}[lang]
    ht_desc={"es":"Ofrece a tus huéspedes y clientes un servicio premium de equipaje y mudanzas. Comisión por reserva, QR para recepción y facturación mensual.","en":"Offer your guests a premium luggage and moving service. Commission per booking, reception QR and monthly invoicing.","de":"Biete deinen Gästen einen Premium-Gepäck- und Umzugsservice. Provision pro Buchung, Rezeptions-QR und monatliche Abrechnung."}[lang]
    bl={"es":["Comisión por cada reserva de tus huéspedes o clientes.","Código QR y material para tu recepción o conserjería.","Un único contacto y facturación mensual sencilla.","Servicio bilingüe (ES·EN·DE) que mejora la experiencia del huésped."],
        "en":["Commission on every booking from your guests or clients.","QR code and materials for your reception or concierge.","One single contact and easy monthly invoicing.","Multilingual service (ES·EN·DE) that improves the guest experience."],
        "de":["Provision bei jeder Buchung deiner Gäste oder Kunden.","QR-Code und Material für deine Rezeption oder Concierge.","Ein einziger Ansprechpartner und einfache monatliche Abrechnung.","Mehrsprachiger Service (ES·EN·DE), der das Gästeerlebnis verbessert."]}[lang]
    blocks='<section class="article"><div class="wrap"><ul>'+"".join(f"<li>{esc(x)}</li>" for x in bl)+"</ul></div></section>"
    build_info("hoteles-y-partners",lang,ht_title,ht_desc,ht_h1,blocks)

    # Contacto
    ct_title={"es":"Contacto y reservas · BaggageGo Mallorca","en":"Contact & booking · BaggageGo Mallorca","de":"Kontakt & Buchung · BaggageGo Mallorca"}[lang]
    ct_h1={"es":"Reserva o pregúntanos","en":"Book or ask us anything","de":"Buchen oder fragen"}[lang]
    ct_desc={"es":"Escríbenos por WhatsApp o email para reservar tu entrega de equipaje o pedir presupuesto de mudanza en Mallorca.","en":"Message us on WhatsApp or email to book your luggage delivery or request a moving quote in Mallorca.","de":"Schreib uns per WhatsApp oder E-Mail, um deine Gepäcklieferung zu buchen oder ein Umzugsangebot auf Mallorca anzufordern."}[lang]
    lbl={"es":("Nombre","¿Qué necesitas?","Tu nombre","Ej: 2 maletas del aeropuerto PMI a un hotel en Sóller el 12 de julio."),
         "en":("Name","What do you need?","Your name","E.g. 2 bags from PMI airport to a hotel in Sóller on July 12."),
         "de":("Name","Was brauchst du?","Dein Name","z.B. 2 Koffer vom Flughafen PMI zu einem Hotel in Sóller am 12. Juli.")}[lang]
    out_ct=LANG_BASE[lang]+INFO_SLUG['contacto'][lang]+'.html'
    blocks=f"""<section><div class="wrap" style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start">
<div><div class="cinfo"><div class="ci"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div><div><b>WhatsApp</b>{esc(PHONE_DISPLAY)}</div></div>
<div class="cinfo"><div class="ci"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></div><div><b>Email</b>{EMAIL}</div></div>
<div class="cinfo"><div class="ci"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 21s-7-6.4-7-11a7 7 0 0114 0c0 4.6-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><div><b>{esc(ui['coverage'])}</b>{esc(CITY)}</div></div></div>
<form class="form" onsubmit="sendForm(event)">
<div class="field"><label style="color:var(--muted)">{esc(lbl[0])}</label><div class="in"><input id="c_name" required placeholder="{esc(lbl[2])}"></div></div>
<div class="field"><label style="color:var(--muted)">Email</label><div class="in"><input id="c_email" type="email" required placeholder="email@email.com"></div></div>
<div class="field"><label style="color:var(--muted)">{esc(lbl[1])}</label><div class="in" style="align-items:flex-start"><textarea id="c_msg" rows="4" placeholder="{esc(lbl[3])}"></textarea></div></div>
<button class="btn btn-primary" type="submit">{esc(ui['send'])}</button></form>
</div></section>"""
    build_info("contacto",lang,ct_title,ct_desc,ct_h1,blocks)

# ---------------------------------------------------------------- SITEMAP + ROBOTS
def build_blog_index(lang):
    out = LANG_BASE[lang] + INFO_SLUG["blog"][lang] + ".html"
    group = "info_blog"
    ui = UI[lang]
    home = LANG_BASE[lang]+"index.html"
    T = {"es":("Guías","Guías de viaje, ciclismo y mudanzas en Mallorca","Consejos para viajar, pedalear y mudarte a Mallorca sin complicaciones.","Leer guía"),
         "en":("Guides","Travel, cycling and moving guides for Mallorca","Tips to travel, ride and move to Mallorca hassle-free.","Read guide"),
         "de":("Ratgeber","Reise-, Rad- und Umzugsratgeber für Mallorca","Tipps, um zu reisen, zu fahren und nach Mallorca zu ziehen – ohne Stress.","Ratgeber lesen")}[lang]
    trail=[(ui["home"],home),(T[0],None)]
    trail_abs=[(ui["home"],url_abs(home)),(T[0],url_abs(out))]
    jl=[jsonld_localbusiness(), jsonld_breadcrumb(trail_abs)]
    H=head(lang,T[1]+" | BaggageGo",T[2],out,group,jl)
    hero=f"""<section class="hero">{breadcrumb(lang,out,trail)}<div class="wrap"><h1>{esc(T[1])}</h1><p class="sub">{esc(T[2])}</p><div style="height:26px"></div></div></section>"""
    cards=""
    for a in BLOG:
        href=rel(out, LANG_BASE[lang]+SEG_BLOG[lang]+"/"+a["slug"][lang]+".html")
        cards+=f'<a class="card" href="{href}"><h3>{esc(a["h1"][lang])}</h3><p>{esc(a["desc"][lang])}</p><span class="more">{esc(T[3])} →</span></a>'
    body=f'<section><div class="wrap"><div class="cards">{cards}</div></div></section>'
    page=H+header(lang,out,group)+hero+body+cta_band(lang,out)+footer(lang,out)
    write(out,page)

def build_article(a, lang):
    out = LANG_BASE[lang] + SEG_BLOG[lang] + "/" + a["slug"][lang] + ".html"
    group = "blog_" + a["id"]
    ui = UI[lang]
    home = LANG_BASE[lang]+"index.html"
    blog_index = LANG_BASE[lang] + INFO_SLUG["blog"][lang] + ".html"
    blog_label = {"es":"Guías","en":"Guides","de":"Ratgeber"}[lang]
    trail=[(ui["home"],home),(blog_label,blog_index),(a["h1"][lang],None)]
    trail_abs=[(ui["home"],url_abs(home)),(blog_label,url_abs(blog_index)),(a["h1"][lang],url_abs(out))]
    jl=[jsonld_localbusiness(), jsonld_breadcrumb(trail_abs),
        '{"@context":"https://schema.org","@type":"Article","headline":%s,"description":%s,"inLanguage":"%s","datePublished":"%s","author":{"@type":"Organization","name":"%s Mallorca"},"publisher":{"@type":"Organization","name":"%s Mallorca"}}' % (_json(a["h1"][lang]), _json(a["desc"][lang]), lang, a["date"], BRAND, BRAND)]
    H=head(lang,a["title"][lang],a["desc"][lang],out,group,jl)
    hero=f"""<section class="hero">{breadcrumb(lang,out,trail)}<div class="wrap"><h1>{esc(a['h1'][lang])}</h1><p class="sub">{esc(a['intro'][lang])}</p><div style="height:26px"></div></div></section>"""
    body='<section class="article"><div class="wrap">'
    for h2,p,li in a["secs"][lang]:
        body+=f"<h2>{esc(h2)}</h2><p>{esc(p)}</p>"
        if li: body+="<ul>"+"".join(f"<li>{esc(x)}</li>" for x in li)+"</ul>"
    body+="</div></section>"
    # related: los servicios ligados al artículo
    rnames={"es":{"aeropuerto":"Entrega de maletas","consigna":"Consigna","ciclistas":"Equipaje para ciclistas","mudanzas":"Mudanzas exprés","mercancias":"Transporte de mercancías","guardamuebles":"Guardamuebles","bicicletas":"Transporte de bicicletas"},
            "en":{"aeropuerto":"Luggage delivery","consigna":"Storage","ciclistas":"Cyclist luggage","mudanzas":"Express moving","mercancias":"Cargo van","guardamuebles":"Storage","bicicletas":"Bike transport"},
            "de":{"aeropuerto":"Gepäcklieferung","consigna":"Aufbewahrung","ciclistas":"Radfahrer-Gepäck","mudanzas":"Express-Umzüge","mercancias":"Warentransport","guardamuebles":"Einlagerung","bicicletas":"Fahrradtransport"}}[lang]
    rcards=""
    for sid in a["rel"]:
        s=next(x for x in SERVICES if x["id"]==sid)
        href=rel(out, LANG_BASE[lang]+SEG[lang]["serv"]+"/"+s["slug"][lang]+".html")
        rcards+=f'<a class="rel" href="{href}">{esc(rnames[sid])} <span class="accent">→</span></a>'
    rel_html=f'<section class="related"><div class="wrap"><div class="sec-head"><h2>{esc(ui["related_s"])}</h2></div><div class="rel-grid">{rcards}</div></div></section>'
    page=H+header(lang,out,group)+hero+body+rel_html+cta_band(lang,out)+footer(lang,out)
    write(out,page)

def build_sitemap():
    urls=""
    for e in sorted(REGISTRY,key=lambda x:-x["prio"]):
        gp=group_paths(e["group"])
        alt=""
        for l in LANGS:
            if l in gp:
                alt+='<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l,url_abs(gp[l]))
        urls+=f'<url><loc>{url_abs(e["path"])}</loc>{alt}<priority>{e["prio"]:.1f}</priority></url>\n'
    sm=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n'
    write("sitemap.xml",sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

# ---------------------------------------------------------------- MAIN
def main():
    # limpiar salida previa (solo carpetas generadas y archivos raiz)
    for sub in ["en","de","servicios","zonas","guias"]:
        p=os.path.join(ROOT,sub)
        if os.path.isdir(p): shutil.rmtree(p)
    for f in ["index.html","styles.css","main.js","sitemap.xml","robots.txt",
              "como-funciona.html","precios.html","hoteles-y-partners.html","contacto.html","guias.html"]:
        fp=os.path.join(ROOT,f)
        if os.path.isfile(fp): os.remove(fp)

    write("styles.css", CSS)
    write("main.js", JS)
    write("CNAME", "baggage-go.com\n")   # dominio personalizado en GitHub Pages
    write(".nojekyll", "")               # servir el HTML tal cual (sin Jekyll)

    # PASO 0: planificar TODAS las rutas (hreflang correcto)
    plan()

    # PASO 1: generar el HTML de cada pagina
    for lang in LANGS:
        build_home(lang)
    for lang in LANGS:
        for s in SERVICES: build_service(s,lang)
        for z in ZONES: build_zone(z,lang)
        build_info_pages(lang)
        build_blog_index(lang)
        for a in BLOG: build_article(a,lang)

    build_sitemap()
    print("Paginas generadas:", len(REGISTRY))
    for e in sorted(REGISTRY,key=lambda x:x["path"]):
        print("  ", e["path"])

if __name__=="__main__":
    main()
