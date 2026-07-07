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
PHONE_DISPLAY = "+34 686 822 291"  # WhatsApp / telefono real
WA = "34686822291"                 # WhatsApp real (sin + ni espacios) para wa.me
EMAIL = "hey@baggage-go.com"       # correo corporativo (Cloudflare Email Routing -> Gmail)
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
   "price_from":"desde","draft":"Servicio en toda Mallorca · Presupuesto sin compromiso.",
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
   "price_from":"from","draft":"Service across Mallorca · Free, no-obligation quote.",
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
   "price_from":"ab","draft":"Service auf ganz Mallorca · Kostenloses Angebot.",
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
  "intro":{"es":"Aterrizas en Palma y lo último que te apetece es pelearte con las maletas. Así que no lo hagas: las recogemos nosotros en la terminal del PMI y las dejamos directamente en tu alojamiento —hotel, villa o apartamento—, estés donde estés en la isla. Tú sales del aeropuerto con las manos libres y te vas derecho a empezar las vacaciones.",
           "en":"You land in Palma and the last thing you want is to wrestle with your bags. So don't. We collect them at the PMI terminal and drop them straight at your accommodation —hotel, villa or apartment—, wherever you are on the island. You walk out of the airport with your hands free and head straight into your holiday.",
           "de":"Du landest in Palma, und das Letzte, worauf du Lust hast, ist der Kampf mit dem Gepäck. Also lass es. Wir holen es am PMI-Terminal ab und bringen es direkt zu deiner Unterkunft —Hotel, Villa oder Apartment—, egal wo auf der Insel du bist. Du verlässt den Flughafen mit freien Händen und startest direkt in den Urlaub."},
  "secs":{
    "es":[("Cómo funciona, paso a paso",
           "Reservas online y nos dices tu vuelo, cuántas maletas traes y adónde van. A partir de ahí nos encargamos nosotros: un conductor recoge tu equipaje y lo lleva a tu alojamiento el mismo día, con seguimiento para que sepas por dónde va y seguro incluido de principio a fin.",
           ["Perfecto para equipaje que abulta: palos de golf, la bici, la tabla de surf.","Un alivio si viajas con niños o te espera un coche de alquiler pequeño.","Y funciona igual a la vuelta: recogemos en el hotel y llevamos tus maletas al aeropuerto para tu salida."]),
          ("¿Por qué cargar con todo si no hace falta?",
           "Desde el primer minuto en Mallorca ganas tiempo y tranquilidad: nada de colas en el parking, ni maleteros que no cierran, ni arrastrar peso bajo el sol con el niño de la mano. Empieza el viaje ligero; de las maletas nos ocupamos nosotros.",[])],
    "en":[("How it works, step by step",
           "You book online and tell us your flight, how many bags you're bringing and where they're going. From there it's on us: a driver picks up your luggage and takes it to your accommodation the same day, with tracking so you know where it is and insurance from start to finish.",
           ["Perfect for bulky kit: golf clubs, the bike, the surfboard.","A relief if you travel with kids or a small rental car is waiting.","And it works just the same on the way back: we collect at the hotel and take your bags to the airport for departure."]),
          ("Why carry it all when you don't have to?",
           "From your very first minute in Mallorca you gain time and peace of mind: no queues at the car park, no boot that won't shut, no dragging weight through the sun with a kid in tow. Start the trip light; we'll look after the bags.",[])],
    "de":[("So läuft es, Schritt für Schritt",
           "Du buchst online und sagst uns deinen Flug, wie viele Gepäckstücke du dabeihast und wohin sie sollen. Ab da übernehmen wir: Ein Fahrer holt dein Gepäck ab und bringt es am selben Tag zu deiner Unterkunft – mit Sendungsverfolgung, damit du weißt, wo es ist, und Versicherung von Anfang bis Ende.",
           ["Ideal für sperriges Zeug: Golfschläger, das Rad, das Surfbrett.","Eine Erleichterung, wenn du mit Kindern reist oder ein kleiner Mietwagen wartet.","Und zurück läuft es genauso: Wir holen im Hotel ab und bringen dein Gepäck zur Abreise an den Flughafen."]),
          ("Warum alles schleppen, wenn es nicht sein muss?",
           "Von der ersten Minute auf Mallorca gewinnst du Zeit und Ruhe: keine Schlange am Parkplatz, kein Kofferraum, der nicht zugeht, kein Schleppen in der Sonne mit dem Kind an der Hand. Starte leicht in den Urlaub; um das Gepäck kümmern wir uns.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta la entrega de maletas desde el aeropuerto?","Desde 14 € por dos maletas puerta a puerta. El precio final depende de la zona de destino y del número de bultos; te lo confirmamos al instante por WhatsApp."),
          ("¿Entregáis el mismo día?","Sí. Con reserva anticipada garantizamos la entrega el mismo día de tu llegada en tu hotel o villa."),
          ("¿El equipaje va asegurado?","Sí, todos los envíos están asegurados y puedes seguir el estado de principio a fin.")],
    "en":[("How much is airport luggage delivery?","From €14 for two bags door to door. The final price depends on the destination area and number of items; we confirm instantly on WhatsApp."),
          ("Do you deliver the same day?","Yes. With advance booking we guarantee same-day delivery to your hotel or villa on your arrival day."),
          ("Is my luggage insured?","Yes, every shipment is insured and you can track its status from start to finish.")],
    "de":[("Was kostet die Gepäcklieferung vom Flughafen?","Ab 14 € für zwei Gepäckstücke von Tür zu Tür. Der Endpreis hängt vom Zielgebiet und der Anzahl der Stücke ab; wir bestätigen sofort per WhatsApp."),
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
  "intro":{"es":"Ese hueco incómodo entre el check-out y el vuelo tiene fácil solución. Déjanos las maletas y disfruta de tus últimas horas en Mallorca como toca: un último baño, una comida con calma o un paseo por el centro, sin arrastrar peso ni estar pendiente del equipaje.",
           "en":"That awkward gap between check-out and your flight has an easy fix. Leave the bags with us and enjoy your last hours in Mallorca the way you should: one more swim, a slow lunch or a stroll through town, with nothing to drag and nothing to keep an eye on.",
           "de":"Diese unbequeme Lücke zwischen Check-out und Flug lässt sich leicht lösen. Lass das Gepäck bei uns und genieße deine letzten Stunden auf Mallorca, wie es sein soll: noch ein Bad, ein entspanntes Essen oder ein Bummel durch die Stadt, ohne etwas zu schleppen und ohne aufs Gepäck aufpassen zu müssen."},
  "secs":{
    "es":[("Guarda por horas o por días, como te venga bien",
           "Nos dejas el equipaje bien guardado y lo recoges cuando quieras. Es la solución perfecta para ese hueco entre el check-out y el vuelo, o entre que llegas y tienes la habitación lista. Ni un minuto perdido cargando maletas.",
           ["Custodia segura y asegurada, con tus cosas en buenas manos.","Sin límite de tamaño: maletas grandes, la bici o el material deportivo caben igual.","Combínalo con nuestra entrega y no vuelves ni a por las maletas: te las llevamos donde digas."]),
          ("La diferencia BaggageGo: guardamos y además te lo llevamos",
           "Una consigna normal te guarda las maletas y ahí se acaba. Nosotros vamos un paso más allá: si quieres, las recogemos, las guardamos y luego te las entregamos donde las necesites, sea el aeropuerto u otro alojamiento. Guardar y llevar, todo con el mismo equipo.",[])],
    "en":[("Store by the hour or by the day, whatever suits you",
           "You leave your luggage safely stored and pick it up whenever you like. It's the perfect fix for that gap between check-out and your flight, or between arriving and your room being ready. Not a minute wasted hauling bags around.",
           ["Safe, insured custody, with your things in good hands.","No size limit: big suitcases, the bike or sports gear all fit just the same.","Combine it with our delivery and you won't even come back for the bags: we bring them to you."]),
          ("The BaggageGo difference: we store, and we bring it to you too",
           "A normal left-luggage point holds your bags and that's where it ends. We go one step further: if you like, we collect them, store them and then deliver them wherever you need, be it the airport or another place to stay. Store and deliver, all with the same team.",[])],
    "de":[("Lagere stundenweise oder tageweise, ganz wie es passt",
           "Du gibst dein Gepäck sicher verwahrt ab und holst es ab, wann du willst. Die perfekte Lösung für die Lücke zwischen Check-out und Flug oder zwischen Ankunft und fertigem Zimmer. Keine Minute mit Kofferschleppen vergeudet.",
           ["Sichere, versicherte Verwahrung – deine Sachen in guten Händen.","Keine Größenbeschränkung: große Koffer, das Rad oder Sportausrüstung passen genauso.","Kombiniere es mit unserer Lieferung, und du kommst nicht mal mehr zurück: Wir bringen dir das Gepäck."]),
          ("Der BaggageGo-Unterschied: Wir lagern und bringen es dir auch",
           "Eine normale Gepäckaufbewahrung verwahrt deine Sachen, und damit ist Schluss. Wir gehen einen Schritt weiter: Wenn du willst, holen wir ab, lagern ein und liefern dann dorthin, wo du es brauchst – ob Flughafen oder andere Unterkunft. Lagern und liefern, alles aus einer Hand.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta la consigna?","Desde 4,90 € por bulto y día (mochila o bolso 2,90 €; bulto especial como bici o golf 7,90 €). Consúltanos por franjas de pocas horas."),
          ("¿Dónde recogéis y entregáis?","En Palma y toda la isla. Podemos recoger en tu hotel y entregar en el aeropuerto o en otro alojamiento.")],
    "en":[("How much is storage?","From €4.90 per bag and day (backpack or handbag €2.90; oversized item such as a bike or golf bag €7.90). Ask us about short few-hour slots."),
          ("Where do you collect and deliver?","In Palma and across the island. We can collect at your hotel and deliver to the airport or another accommodation.")],
    "de":[("Was kostet die Aufbewahrung?","Ab 4,90 € pro Gepäckstück und Tag (Rucksack oder Handtasche 2,90 €; Sperrgut wie Fahrrad oder Golf 7,90 €). Frag uns nach kurzen Zeitfenstern von wenigen Stunden."),
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
  "intro":{"es":"Haces la Tramuntana por etapas, subiendo puertos y cambiando de hotel cada noche. Lo bonito es rodar o caminar; lo pesado, arrastrar la maleta de un pueblo a otro. De eso nos ocupamos nosotros: llevamos tu equipaje —y tu bicicleta— al siguiente alojamiento mientras tú disfrutas del camino ligero.",
           "en":"You're riding or hiking the Tramuntana in stages, climbing the passes and switching hotels each night. The good part is the ride; the heavy part is dragging a suitcase from one village to the next. That's ours to handle: we take your luggage —and your bike— to the next place while you enjoy the route with nothing on your back.",
           "de":"Du machst die Tramuntana in Etappen, kletterst die Pässe hoch und wechselst jede Nacht das Hotel. Das Schöne ist die Tour; das Schwere ist, den Koffer von Dorf zu Dorf zu schleppen. Das übernehmen wir: Wir bringen dein Gepäck – und dein Fahrrad – zur nächsten Unterkunft, während du die Strecke ohne Ballast genießt."},
  "secs":{
    "es":[("De hotel a hotel por la Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... Nos das tu itinerario y nos encargamos del resto: recogemos en tu hotel por la mañana y dejamos las maletas en el siguiente antes de que llegues tú. Cuando entras por la puerta, tus cosas ya están esperándote.",
           ["Movemos bicis de carretera y de montaña, con el mismo cuidado que tus maletas.","Nos ajustamos a tu plan de etapas, sin que tengas que estar pendiente.","Es nuestra temporada fuerte: primavera y otoño, cuando la isla se llena de ciclistas."]),
          ("Y si venís en grupo, mejor todavía",
           "Trabajamos codo con codo con grupos ciclistas y tour operadores que organizan rutas por Mallorca. Un solo contacto para todas las etapas y todos los coches: tú te centras en pedalear, nosotros en que cada maleta llegue a su sitio.",[])],
    "en":[("From hotel to hotel across the Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... You give us your itinerary and we take care of the rest: we collect at your hotel in the morning and drop the bags at the next one before you get there. By the time you walk in, your things are already waiting.",
           ["We move road and mountain bikes with the same care as your bags.","We fit around your stage plan, so you never have to chase it.","It's our busy season: spring and autumn, when the island fills up with riders."]),
          ("And if you come as a group, even better",
           "We work hand in hand with cycling groups and tour operators running routes across Mallorca. One single contact for every stage and every rider: you focus on the pedalling, we make sure each bag lands where it should.",[])],
    "de":[("Von Hotel zu Hotel durch die Serra de Tramuntana",
           "Sóller, Deià, Valldemossa, Pollença... Du gibst uns deine Route, und wir kümmern uns um den Rest: Wir holen morgens im Hotel ab und bringen das Gepäck ins nächste, bevor du dort ankommst. Wenn du zur Tür hereinkommst, warten deine Sachen schon.",
           ["Wir bewegen Renn- und Mountainbikes mit derselben Sorgfalt wie dein Gepäck.","Wir richten uns nach deinem Etappenplan, ohne dass du etwas nachhalten musst.","Es ist unsere Hauptsaison: Frühling und Herbst, wenn sich die Insel mit Radfahrern füllt."]),
          ("Und als Gruppe? Umso besser",
           "Wir arbeiten Hand in Hand mit Radgruppen und Reiseveranstaltern, die Touren über Mallorca organisieren. Ein einziger Ansprechpartner für alle Etappen und alle Fahrer: Du konzentrierst dich aufs Treten, wir darauf, dass jedes Gepäckstück am richtigen Ort ankommt.",[])],
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
  "intro":{"es":"Cambiar de casa dentro de la isla no tiene por qué ser un dolor de cabeza. BaggageGo Moving se encarga de mudanzas pequeñas y exprés —pisos, estudios y oficinas— con el mismo cuidado y la misma seriedad que ponemos en cada maleta. Tú decides el día; nosotros hacemos que salga rodado.",
           "en":"Moving house within the island doesn't have to be a headache. BaggageGo Moving handles small and express moves —flats, studios and offices— with the same care and the same seriousness we put into every suitcase. You pick the day; we make it go smoothly.",
           "de":"Ein Umzug innerhalb der Insel muss kein Kopfzerbrechen sein. BaggageGo Moving übernimmt kleine und Express-Umzüge —Wohnungen, Studios und Büros— mit derselben Sorgfalt und Ernsthaftigkeit, die wir in jeden Koffer stecken. Du wählst den Tag; wir sorgen dafür, dass alles glattläuft."},
  "secs":{
    "es":[("Rápido, cuidado y sin sobresaltos",
           "Va perfecto para mudanzas de última hora, pisos de una a tres habitaciones y oficinas pequeñas. Reservas en un momento, te embalamos si quieres y tratamos tus cosas como si fueran nuestras. Nada de sorpresas el día de la mudanza.",
           ["Mudanzas locales por toda Mallorca, de punta a punta de la isla.","Un mueble suelto, la nevera o cuatro cosas: también las movemos.","Presupuesto claro desde el principio, sin letra pequeña."]),
          ("Hablamos tu idioma, literalmente",
           "Te atendemos en español, inglés y alemán, sin malentendidos. Y eso importa: a Mallorca llega cada año mucha gente de fuera que se instala aquí, y saber que quien te lleva las cosas te entiende quita mucha presión.",[])],
    "en":[("Fast, careful and without nasty surprises",
           "It's spot on for last-minute moves, one to three-bedroom flats and small offices. You book in a moment, we pack for you if you like, and we treat your things as if they were ours. No surprises on moving day.",
           ["Local moves across the whole of Mallorca, end to end.","A single item, the fridge or just a few things: we move those too.","A clear quote from the start, no small print."]),
          ("We speak your language, literally",
           "We look after you in Spanish, English and German, with no misunderstandings. And that matters: plenty of people from abroad settle in Mallorca each year, and knowing the people moving your things actually understand you takes a lot of the pressure off.",[])],
    "de":[("Schnell, sorgfältig und ohne böse Überraschungen",
           "Ideal für kurzfristige Umzüge, Wohnungen mit ein bis drei Zimmern und kleine Büros. Du buchst im Handumdrehen, wir verpacken auf Wunsch für dich, und wir behandeln deine Sachen, als wären es unsere. Keine Überraschungen am Umzugstag.",
           ["Lokale Umzüge auf ganz Mallorca, von einem Ende zum anderen.","Ein einzelnes Möbelstück, der Kühlschrank oder nur ein paar Dinge: bewegen wir auch.","Ein klares Angebot von Anfang an, kein Kleingedrucktes."]),
          ("Wir sprechen deine Sprache, im wörtlichen Sinn",
           "Wir betreuen dich auf Spanisch, Englisch und Deutsch, ohne Missverständnisse. Und das zählt: Jedes Jahr lässt sich viele Menschen aus dem Ausland auf Mallorca nieder, und zu wissen, dass die Leute, die deine Sachen tragen, dich wirklich verstehen, nimmt viel Druck raus.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta una mudanza pequeña?","Una mini mudanza (estudio o pocas cajas) va desde 390 €, y un piso de 2 habitaciones desde 690 €. Preparamos un presupuesto a medida según volumen, distancia y extras."),
          ("¿Hacéis mudanzas a la península o internacionales?","Coordinamos traslados a península e internacionales mediante grupaje; pídenos presupuesto."),
          ("¿Hacéis mudanzas urgentes o mini mudanzas?","Sí. Hacemos mudanzas urgentes, exprés y mini mudanzas de pisos pequeños, estudios o habitaciones sueltas, con reserva rápida y precio cerrado.")],
    "en":[("How much is a small move?","A mini move (studio or a few boxes) starts from €390, and a 2-bedroom flat from €690. We prepare a custom quote based on volume, distance and extras."),
          ("Do you do moves to the mainland or international?","We coordinate mainland and international moves via groupage; ask us for a quote."),
          ("Do you do urgent or small (mini) moves?","Yes. We do urgent, express and mini moves of small flats, studios or single rooms, with quick booking and a fixed price.")],
    "de":[("Was kostet ein kleiner Umzug?","Ein Mini-Umzug (Studio oder wenige Kartons) beginnt ab 390 €, eine 2-Zimmer-Wohnung ab 690 €. Wir erstellen ein individuelles Angebot nach Umfang, Entfernung und Extras."),
          ("Macht ihr Umzüge aufs Festland oder international?","Wir koordinieren Festland- und internationale Umzüge per Sammelladung; frag uns nach einem Angebot."),
          ("Macht ihr dringende Umzüge oder Mini-Umzüge?","Ja. Wir machen dringende, Express- und Mini-Umzüge von kleinen Wohnungen, Studios oder einzelnen Zimmern, mit schneller Buchung und Festpreis.")],
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
  "intro":{"es":"Tienes que mover mercancía, material o un envío que no cabe en un coche y no sabes a quién llamar. Aquí lo tienes claro: te ponemos una furgoneta con conductor cuando la necesites, con la seriedad y el trato de una empresa de transporte que lleva años en esto. Tú nos dices qué y adónde; nosotros lo llevamos.",
           "en":"You've got goods, materials or a shipment that won't fit in a car and you're not sure who to call. Here it's simple: we put a cargo van with driver at your disposal whenever you need it, with the reliability and manner of a transport company that's been doing this for years. You tell us what and where; we take it there.",
           "de":"Du musst Waren, Material oder eine Sendung bewegen, die nicht ins Auto passt, und weißt nicht, wen du anrufen sollst. Hier ist es einfach: Wir stellen dir einen Transporter mit Fahrer bereit, wann immer du ihn brauchst – mit der Zuverlässigkeit und Art eines Transportunternehmens, das seit Jahren dabei ist. Du sagst uns, was und wohin; wir bringen es hin."},
  "secs":{
    "es":[("Una furgoneta con conductor para casi todo","Reparto de mercancía, entregas de última milla, material para un evento, muebles o cualquier envío que se te resista en el coche. Un solo contacto, sin complicaciones, y si eres empresa te lo facturamos de forma sencilla para que no te compliques la contabilidad.",
           ["Un día suelto o rutas fijas cada semana: como mejor te encaje.","Última milla y paquetería voluminosa, esa que nadie quiere subir por las escaleras.","Cubrimos toda Mallorca y tu mercancía va asegurada de principio a fin."]),
          ("Para empresas y también para particulares","Nos llaman comercios, organizadores de eventos y particulares que necesitan mover algo ya, sin el lío ni el coste de contratar un camión entero. Traes lo que sea; nosotros ponemos la furgoneta y el conductor.",[])],
    "en":[("A cargo van with driver for just about anything","Goods distribution, last-mile deliveries, kit for an event, furniture or any shipment that won't behave in a car. One contact, no fuss, and if you're a business we invoice it simply so your accounts stay easy.",
           ["A single day or fixed weekly routes: whatever fits you best.","Last-mile and bulky parcels, the ones nobody wants to carry up the stairs.","We cover the whole of Mallorca and your goods are insured from start to finish."]),
          ("For businesses, and for individuals too","Shops, event organisers and individuals call us when they need to move something now, without the hassle or cost of hiring a whole truck. You bring whatever it is; we bring the van and the driver.",[])],
    "de":[("Ein Transporter mit Fahrer für fast alles","Warenverteilung, Lieferungen auf der letzten Meile, Ausrüstung für ein Event, Möbel oder jede Sendung, die im Auto nicht mitspielt. Ein Ansprechpartner, kein Aufwand, und als Unternehmen rechnen wir es dir einfach ab, damit deine Buchhaltung leicht bleibt.",
           ["Ein einzelner Tag oder feste Routen pro Woche: ganz wie es dir passt.","Letzte Meile und sperrige Pakete – die, die niemand die Treppe hochtragen will.","Wir decken ganz Mallorca ab, und deine Ware ist von Anfang bis Ende versichert."]),
          ("Für Unternehmen und auch für Privatpersonen","Geschäfte, Eventorganisatoren und Privatpersonen rufen uns an, wenn sie sofort etwas bewegen müssen, ohne den Aufwand und die Kosten eines ganzen Lkw. Du bringst, was es auch ist; wir bringen Transporter und Fahrer.",[])],
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
  "intro":{"es":"A veces las fechas no cuadran: te vas de una casa antes de entrar en la otra, o la reforma se alarga y no sabes dónde meter los muebles mientras tanto. Tranquilo, para eso estamos. Guardamos tus cosas en un almacén seguro el tiempo que haga falta y te las llevamos de vuelta el día que estés listo.",
           "en":"Sometimes the dates just don't line up: you leave one place before you can move into the next, or the renovation drags on and you've nowhere to put the furniture in the meantime. Relax, that's what we're here for. We keep your things in secure storage for as long as you need and bring them back the day you're ready.",
           "de":"Manchmal passen die Termine einfach nicht: Du ziehst aus, bevor du in die nächste Wohnung kannst, oder die Renovierung zieht sich und du weißt nicht, wohin mit den Möbeln. Keine Sorge, dafür sind wir da. Wir lagern deine Sachen sicher ein, so lange du brauchst, und bringen sie zurück, sobald du bereit bist."},
  "secs":{
    "es":[("Guarda por meses, el tiempo que haga falta","Muebles, cajas o stock: los guardamos el tiempo que necesites, ni un día de más. Y no tienes ni que acercarte al almacén, porque recogemos y entregamos en tu puerta. Es la solución perfecta para ese hueco entre dos mudanzas o mientras dura una reforma.",
           ["Custodia segura y asegurada, con tus cosas a buen recaudo.","Recogida y entrega a domicilio: nosotros vamos, tú no te mueves.","Y si además te mudas, lo enlazamos con tu mudanza BaggageGo Moving en un solo servicio."]),
          ("Para quien se instala y para quien tiene un negocio","Va de perlas si te estás mudando y necesitas ganar tiempo, y también para comercios que quieren quitarse de en medio el stock de temporada hasta que vuelva a hacer falta.",[])],
    "en":[("Store by the month, for as long as you need","Furniture, boxes or stock: we keep them for as long as you need, not a day more. And you don't even have to go near the warehouse, because we collect and deliver to your door. It's the perfect fix for that gap between two moves or while a renovation runs its course.",
           ["Safe, insured custody, with your things kept well out of harm's way.","Home pick-up and delivery: we come to you, you stay put.","And if you're moving too, we tie it into your BaggageGo Moving move as a single service."]),
          ("For people settling in and for people running a business","It's a lifesaver if you're mid-move and need to buy time, and just as handy for shops wanting seasonal stock out of the way until it's needed again.",[])],
    "de":[("Lagere monatsweise, so lange du brauchst","Möbel, Kartons oder Warenbestand: Wir verwahren sie, so lange du brauchst, keinen Tag länger. Und du musst nicht mal zum Lager, denn wir holen ab und liefern an deine Tür. Die perfekte Lösung für die Lücke zwischen zwei Umzügen oder während einer Renovierung.",
           ["Sichere, versicherte Verwahrung – deine Sachen gut aufgehoben.","Abholung und Lieferung nach Hause: Wir kommen zu dir, du bleibst, wo du bist.","Und wenn du auch umziehst, verbinden wir es mit deinem BaggageGo Moving Umzug zu einem einzigen Service."]),
          ("Für alle, die sich einleben, und für alle mit einem Geschäft","Ein Segen, wenn du mitten im Umzug steckst und Zeit gewinnen musst, und genauso praktisch für Geschäfte, die saisonalen Warenbestand aus dem Weg haben wollen, bis er wieder gebraucht wird.",[])],
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
  "intro":{"es":"Mallorca es de esos sitios con los que sueña cualquier ciclista, pero mover la bici por la isla con la funda a cuestas es lo menos divertido del viaje. Ahí entramos nosotros: la recogemos en el aeropuerto, te la llevamos al hotel y la movemos entre alojamientos, para que tú solo tengas que pensar en rodar.",
           "en":"Mallorca is one of those places every cyclist dreams about, but hauling your bike around the island in its bag is the least fun part of the trip. That's where we come in: we collect it at the airport, take it to your hotel and move it between places to stay, so all you have to think about is riding.",
           "de":"Mallorca ist einer dieser Orte, von denen jeder Radfahrer träumt, aber das Rad in der Tasche über die Insel zu schleppen ist der langweiligste Teil der Reise. Genau hier kommen wir ins Spiel: Wir holen es am Flughafen ab, bringen es zu deinem Hotel und bewegen es zwischen Unterkünften, damit du nur ans Fahren denken musst."},
  "secs":{
    "es":[("Del aeropuerto al hotel y de etapa en etapa","Movemos bicis de carretera y de montaña, en caja o montadas, tratándolas con el cuidado que se merecen (sabemos lo que vale una buena bici). Nos ajustamos a tu ruta por la Tramuntana para que la tuya esté siempre donde tú vas a estar.",
           ["Te la recogemos en el aeropuerto PMI nada más aterrizar.","La llevamos de un hotel al siguiente si haces la isla por etapas.","Y si venís club, grupo o con un tour operador, lo coordinamos todo desde un solo contacto."]),
          ("Y de paso, tu equipaje también","No tiene sentido que la bici viaje sola. Movemos bici y maletas a la vez para que tú vayas del todo ligero, con las manos libres y la cabeza en la carretera.",[])],
    "en":[("From the airport to your hotel and stage by stage","We move road and mountain bikes, boxed or assembled, handling them with the care they deserve (we know what a good bike is worth). We fit around your Tramuntana route so yours is always where you're going to be.",
           ["We collect it at PMI airport the moment you land.","We take it from one hotel to the next if you're riding the island in stages.","And if you're a club, a group or with a tour operator, we coordinate it all through one contact."]),
          ("And your luggage along with it","There's no sense in the bike travelling alone. We move bike and bags together so you travel completely light, hands free and mind on the road.",[])],
    "de":[("Vom Flughafen zum Hotel und Etappe für Etappe","Wir bewegen Renn- und Mountainbikes, verpackt oder montiert, und behandeln sie mit der Sorgfalt, die sie verdienen (wir wissen, was ein gutes Rad wert ist). Wir richten uns nach deiner Tramuntana-Route, damit deins immer dort ist, wo du sein wirst.",
           ["Wir holen es am Flughafen PMI ab, sobald du landest.","Wir bringen es von einem Hotel zum nächsten, wenn du die Insel in Etappen fährst.","Und als Verein, Gruppe oder mit einem Reiseveranstalter koordinieren wir alles über einen Ansprechpartner."]),
          ("Und dein Gepäck gleich mit","Es ergibt keinen Sinn, dass das Rad allein reist. Wir bewegen Fahrrad und Gepäck zusammen, damit du völlig leicht unterwegs bist – freie Hände, Kopf auf der Straße.",[])],
  },
  "faq":{
    "es":[("¿Transportáis la bici desde el aeropuerto?","Sí, recogemos tu bicicleta en el aeropuerto PMI y la entregamos en tu hotel o villa, montada o en caja."),
          ("¿Cuánto cuesta el transporte de una bicicleta?","Desde 19 € por bici y día. Para grupos y varias etapas preparamos un presupuesto a medida (pack ciclista semanal desde 99 €).")],
    "en":[("Do you transport the bike from the airport?","Yes, we collect your bike at PMI airport and deliver it to your hotel or villa, assembled or boxed."),
          ("How much is bike transport?","From €19 per bike and day. For groups and multiple stages we prepare a custom quote (weekly cyclist pack from €99).")],
    "de":[("Transportiert ihr das Fahrrad vom Flughafen?","Ja, wir holen dein Fahrrad am Flughafen PMI ab und liefern es zu deinem Hotel oder deiner Villa, montiert oder verpackt."),
          ("Was kostet der Fahrradtransport?","Ab 19 € pro Rad und Tag. Für Gruppen und mehrere Etappen erstellen wir ein individuelles Angebot (Wochenpaket für Radfahrer ab 99 €).")],
  },
 },
 {
  "id":"portes",
  "slug":{"es":"portes-palma-mallorca","en":"man-with-a-van-mallorca","de":"moebeltransport-mallorca"},
  "icon":'<path d="M12 3l8 4v8l-8 4-8-4V7z"/><path d="M4 7l8 4 8-4M12 11v8"/>',
  "title":{"es":"Portes en Palma de Mallorca: muebles y mini mudanzas | BaggageGo",
           "en":"Man with a van in Mallorca: furniture & small moves | BaggageGo",
           "de":"Möbeltransport auf Mallorca: Möbel & kleine Umzüge | BaggageGo"},
  "desc":{"es":"Portes económicos en Palma de Mallorca: transporte de muebles sueltos, mini mudanzas, sofás, colchones y compras de IKEA. Rápido, urgente y asegurado.",
          "en":"Man with a van in Mallorca: transport of single furniture items, small moves, sofas, mattresses and IKEA purchases. Fast, urgent and insured.",
          "de":"Möbeltransport auf Mallorca: Einzelmöbel, kleine Umzüge, Sofas, Matratzen und IKEA-Einkäufe. Schnell, dringend und versichert."},
  "h1":{"es":"Portes en Palma de Mallorca","en":"Man with a van in Mallorca","de":"Möbeltransport auf Mallorca"},
  "intro":{"es":"Ese sofá nuevo, el colchón que no entra en el coche o las cuatro cajas que tienes que cambiar de piso no merecen el lío de contratar un camión entero. Para eso está un buen porte: rápido, a buen precio y, si te corre prisa, en el mismo día. En Palma y en toda Mallorca, tú nos dices qué hay que mover y nosotros aparecemos con la furgoneta.",
           "en":"That new sofa, the mattress that won't fit in the car or the few boxes you need to shift to another flat don't warrant the hassle of hiring a whole truck. That's what a good man with a van is for: fast, well priced and, if you're in a hurry, same day. In Palma and across Mallorca, you tell us what needs moving and we show up with the van.",
           "de":"Das neue Sofa, die Matratze, die nicht ins Auto passt, oder die paar Kartons, die in eine andere Wohnung müssen, sind keinen ganzen Lkw wert. Genau dafür gibt es einen guten Möbeltransport: schnell, günstig und, wenn es eilt, am selben Tag. In Palma und auf ganz Mallorca sagst du uns, was zu bewegen ist, und wir tauchen mit dem Transporter auf."},
  "secs":{
    "es":[("Portes y muebles sueltos, sin dramas","Sofás, colchones, electrodomésticos, cajas o ese mueble raro que no sabes cómo mover: lo llevamos de un punto a otro y ya está. Es justo lo que necesitas después de una compra en IKEA o Leroy Merlín, para cerrar una venta de segunda mano o para un traslado puntual que no da para una mudanza.",
           ["Vamos con furgoneta y conductor, y si el mueble pesa, con un ayudante.","¿Te corre prisa? Hacemos portes urgentes y en el mismo día si hay hueco.","Y si lo necesitas, montamos y desmontamos el mueble, no solo lo movemos."]),
          ("Mini mudanzas: lo justo, sin pagar de más","Para un estudio, una habitación o un piso pequeño, montar una mudanza completa es matar moscas a cañonazos. Una mini mudanza es más rápida, más barata y se reserva en un momento, con precio cerrado y sin sorpresas al final.",[])],
    "en":[("Single items, moved without the drama","Sofas, mattresses, appliances, boxes or that awkward piece you've no idea how to shift: we take it from one place to another and that's that. It's exactly what you need after an IKEA or Leroy Merlín run, to close a second-hand sale, or for a one-off move that doesn't warrant a full removal.",
           ["We come with a van and driver, and if it's heavy, a helper too.","In a rush? We do urgent and same-day jobs whenever there's a slot.","And if you need it, we assemble and disassemble the furniture, not just move it."]),
          ("Small moves: just enough, without overpaying","For a studio, a single room or a small flat, arranging a full removal is using a sledgehammer to crack a nut. A small move is quicker, cheaper and booked in a moment, with a fixed price and no surprises at the end.",[])],
    "de":[("Einzelstücke, bewegt ohne Drama","Sofas, Matratzen, Geräte, Kartons oder dieses sperrige Teil, bei dem du keine Ahnung hast, wie du es bewegen sollst: Wir bringen es von einem Ort zum anderen, fertig. Genau das, was du nach einem IKEA- oder Leroy-Merlín-Einkauf brauchst, um einen Gebrauchtverkauf abzuschließen oder für einen einmaligen Transport, der keinen kompletten Umzug wert ist.",
           ["Wir kommen mit Transporter und Fahrer, und wenn es schwer ist, mit einem Helfer.","Eilt es? Wir machen dringende Transporte am selben Tag, sofern ein Platz frei ist.","Und wenn du willst, bauen wir das Möbel auf und ab, nicht nur bewegen wir es."]),
          ("Mini-Umzüge: genau das Richtige, ohne zu viel zu zahlen","Für ein Studio, ein einzelnes Zimmer oder eine kleine Wohnung ist ein kompletter Umzug mit Kanonen auf Spatzen geschossen. Ein Mini-Umzug ist schneller, günstiger und im Handumdrehen gebucht, mit Festpreis und ohne Überraschungen am Ende.",[])],
  },
  "faq":{
    "es":[("¿Cuánto cuesta un porte en Palma de Mallorca?","Un porte va desde 49 € la primera hora (hora extra +35 €), según el volumen y la urgencia. Cuéntanos qué necesitas mover y te damos precio al momento."),
          ("¿Hacéis portes urgentes o en el mismo día?","Sí, ofrecemos portes urgentes y en el día siempre que haya disponibilidad.")],
    "en":[("How much is a man with a van in Mallorca?","A man-with-a-van job starts from €49 for the first hour (extra hour +€35), depending on volume and urgency. Tell us what you need to move and we quote right away."),
          ("Do you do urgent or same-day jobs?","Yes, we offer urgent and same-day service subject to availability.")],
    "de":[("Was kostet ein Möbeltransport auf Mallorca?","Ein Möbeltransport beginnt bei 49 € für die erste Stunde (weitere Stunde +35 €), je nach Umfang und Dringlichkeit. Sag uns, was du bewegen musst, und wir nennen sofort den Preis."),
          ("Macht ihr dringende Transporte am selben Tag?","Ja, wir bieten dringenden Service am selben Tag, sofern verfügbar.")],
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
  "intro":{"es":"Mallorca es, probablemente, el mejor sitio de Europa para rodar en primavera y otoño: puertos míticos de la Serra de Tramuntana, carreteras impecables y un clima que acompaña. Si estás preparando tu viaje ciclista, la gran pregunta es siempre la misma: ¿me traigo mi bici o la alquilo aquí? Te lo contamos claro, y de paso te explicamos cómo moverla por la isla sin que tengas que cargar con nada.","en":"For riding in spring and autumn, Mallorca is hard to beat: the legendary climbs of the Serra de Tramuntana, flawless tarmac and weather that plays along. If you are planning a cycling trip, the big question is always the same — bring your own bike or rent one here? Here is the honest answer, plus how we take the hassle of moving it out of your hands entirely.","de":"Zum Radfahren im Frühling und Herbst ist Mallorca kaum zu schlagen: die legendären Anstiege der Serra de Tramuntana, tadelloser Asphalt und Wetter, das mitspielt. Wenn du deine Radreise planst, ist die große Frage immer dieselbe — eigenes Rad mitbringen oder hier mieten? Hier die ehrliche Antwort, und dazu, wie wir dir das Bewegen des Rads komplett abnehmen."},
  "secs":{
    "es":[("¿Traer tu bici o alquilarla?","No hay una respuesta única, depende de ti. Traer la tuya es lo más cómodo a nivel de sensaciones: conoces cada marcha y cada centímetro del sillín, y eso en un puerto largo se nota. A cambio, toca facturarla en el avión, pagar el suplemento y embalarla con cuidado. Alquilar te ahorra ese lío, y aquí hay tiendas excelentes, pero nunca es del todo tu bici. Por norma, quien viene a hacer rutas largas y exigentes por la Tramuntana suele traer la suya; quien busca un par de salidas tranquilas, alquila sin pensarlo.",[]),
          ("Facturar la bicicleta en el avión","Si te la traes, revisa con tiempo la política de tu aerolínea: cada una tiene sus medidas, su peso máximo y su tarifa, y conviene reservar el transporte de la bici al comprar el vuelo. Desmóntala lo justo (pedales, manillar, ruedas si hace falta) y protégela bien en una funda acolchada o, mejor aún, en una maleta rígida. Un buen embalaje es la diferencia entre llegar y rodar o llegar y buscar un taller.",[]),
          ("Muévela por la isla sin cargarla","Y aquí entramos nosotros. Una vez en Mallorca, recogemos tu bici en el aeropuerto y te la llevamos al hotel, montada y lista. Si haces una ruta por etapas y cambias de alojamiento cada noche, movemos la bici (y tu equipaje) al siguiente hotel mientras tú pedaleas ligero. Tú disfrutas del puerto; de la logística nos encargamos nosotros.",[])],
    "en":[("Bring your bike or rent one?","There is no single right answer — it comes down to you. Bringing your own wins on feel: you know every gear and every millimetre of that saddle, and on a long climb that really counts. The trade-off is checking it in, paying the airline fee and packing it carefully. Renting skips all that, and Mallorca has some excellent bike shops, but it is never quite your own bike. As a rule, riders here for long, demanding Tramuntana routes tend to bring their own; those after a couple of relaxed rides simply rent.",[]),
          ("Checking your bike on the plane","If you do bring it, check your airline policy early: each one has its own size and weight limits and its own fee, and it is best to book the bike on when you buy the flight. Strip it down just enough (pedals, handlebars, wheels if needed) and protect it well in a padded bag or, better still, a hard case. Good packing is the difference between landing and riding, or landing and hunting for a workshop.",[]),
          ("Move it around the island without carrying it","This is where we come in. Once you are in Mallorca, we collect your bike at the airport and bring it to your hotel, assembled and ready. If you are riding a multi-stage route and changing hotels each night, we move the bike (and your luggage) to the next one while you ride light. You enjoy the climb; we handle the logistics.",[])],
    "de":[("Eigenes Rad mitbringen oder mieten?","Es gibt keine einzig richtige Antwort — es hängt von dir ab. Das eigene Rad gewinnt beim Gefühl: Du kennst jeden Gang und jeden Millimeter deines Sattels, und an einem langen Anstieg zählt das wirklich. Der Preis dafür: Aufgabe am Flughafen, die Gebühr der Airline und sorgfältiges Verpacken. Mieten erspart dir das alles, und Mallorca hat hervorragende Radläden, aber es ist nie ganz dein eigenes Rad. In der Regel bringen Fahrer für lange, anspruchsvolle Tramuntana-Routen ihr eigenes mit; wer ein paar entspannte Ausfahrten sucht, mietet einfach.",[]),
          ("Das Fahrrad im Flugzeug aufgeben","Wenn du es mitbringst, prüfe früh die Regeln deiner Airline: Jede hat eigene Maße, ein Höchstgewicht und ihre Gebühr, und du buchst das Rad am besten schon beim Flug mit. Zerlege es nur so weit wie nötig (Pedale, Lenker, bei Bedarf Räder) und schütze es gut in einer gepolsterten Tasche oder besser in einem Hartschalenkoffer. Gutes Verpacken ist der Unterschied zwischen Ankommen und Losfahren oder Ankommen und eine Werkstatt suchen.",[]),
          ("Beweg es über die Insel, ohne es zu tragen","Und hier kommen wir ins Spiel. Auf Mallorca holen wir dein Rad am Flughafen ab und bringen es montiert und startklar zu deinem Hotel. Fährst du eine Etappenroute und wechselst jede Nacht die Unterkunft, bringen wir das Rad (und dein Gepäck) zum nächsten Hotel, während du leicht fährst. Du genießt den Anstieg; um die Logistik kümmern wir uns.",[])],
  }},
 {"id":"mudarse","date":"2026-04-20","rel":["mudanzas","guardamuebles"],
  "slug":{"es":"guia-para-mudarse-a-mallorca","en":"guide-to-moving-to-mallorca","de":"umzug-nach-mallorca-ratgeber"},
  "title":{"es":"Guía para mudarse a Mallorca (residentes y extranjeros) | BaggageGo","en":"Guide to moving to Mallorca (residents and expats) | BaggageGo","de":"Umzug nach Mallorca: Ratgeber für Auswanderer | BaggageGo"},
  "desc":{"es":"Todo lo que necesitas para mudarte a Mallorca: cómo organizar el traslado de tus muebles, el papeleo básico y opciones de guardamuebles mientras te instalas.","en":"Everything you need to move to Mallorca: how to organise your furniture transport, basic paperwork and storage options while you settle in.","de":"Alles für deinen Umzug nach Mallorca: wie du deinen Möbeltransport organisierst, grundlegende Formalitäten und Einlagerungsoptionen, während du dich einlebst."},
  "h1":{"es":"Guía para mudarse a Mallorca","en":"Guide to moving to Mallorca","de":"Umzug nach Mallorca: der Ratgeber"},
  "intro":{"es":"Cada año, miles de personas deciden que Mallorca sea su casa, muchas de ellas alemanas y británicas. Y llegar a una isla (o cambiar de casa dentro de ella) siempre trae papeleo y logística. Si te instalas aquí, esta guía te ordena las ideas para que la mudanza sea lo de menos y disfrutes cuanto antes de vivir en Mallorca.","en":"Every year, thousands of people decide to make Mallorca home — many of them German and British. And moving to an island (or across it) always comes with paperwork and logistics. If you are settling here, this guide clears up the essentials so the move becomes the easy part and you can start enjoying island life sooner.","de":"Jedes Jahr entscheiden sich Tausende, Mallorca zu ihrem Zuhause zu machen, viele davon Deutsche und Briten. Und der Umzug auf eine Insel (oder über sie hinweg) bringt immer Papierkram und Logistik mit sich. Wenn du dich hier niederlässt, bringt dieser Ratgeber Ordnung ins Wesentliche, damit der Umzug zur leichtesten Übung wird und du das Inselleben früher genießt."},
  "secs":{
    "es":[("Planifica el traslado de tus muebles","Lo primero es decidir con cabeza qué merece la pena traer y qué es más fácil comprar aquí. Si vienes de la península o del extranjero, el grupaje (compartir camión con otros envíos) abarata muchísimo el transporte, aunque tarde algo más. Y una vez en la isla, una mudanza local es rápida y sale bien de precio; para cuatro cosas, hasta un porte exprés te resuelve el día.",[]),
          ("Papeleo básico al llegar","En paralelo, ve avanzando con los trámites: empadronamiento en tu ayuntamiento, NIE si aún no lo tienes y alta de suministros (luz, agua, internet). El consejo de quien ya ha pasado por ello: consigue una dirección fija cuanto antes, porque casi todo lo demás depende de tenerla.",[]),
          ("Guardamuebles mientras te instalas","¿Todavía no tienes casa definitiva o entras en obras? No pasa nada. Guardamos tus muebles unos meses en un almacén seguro y te los llevamos de vuelta el día que estés listo. Así te mudas sin prisas y sin tener el salón lleno de cajas.",[])],
    "en":[("Plan your furniture transport","Start by deciding, sensibly, what is worth bringing and what is easier to buy once you are here. Coming from the mainland or abroad, groupage (sharing a truck with other shipments) cuts the cost of transport dramatically, even if it takes a little longer. And once on the island, a local move is quick and good value; for just a few things, an express man-with-a-van sorts your day.",[]),
          ("Basic paperwork on arrival","In parallel, get the admin moving: town-hall registration (empadronamiento), your NIE if you do not have one yet, and utility contracts (electricity, water, internet). One tip from people who have done it: get a fixed address as early as you can, because almost everything else depends on having one.",[]),
          ("Storage while you settle in","Still without a permanent home, or waiting on renovations? No problem. We keep your furniture in secure storage for a few months and bring it back the day you are ready. That way you move at your own pace, without a living room full of boxes.",[])],
    "de":[("Plane deinen Möbeltransport","Überlege zuerst mit Bedacht, was sich mitzubringen lohnt und was du besser hier kaufst. Vom Festland oder aus dem Ausland senkt Sammelladung (ein Lkw, den du mit anderen Sendungen teilst) die Transportkosten enorm, auch wenn es etwas länger dauert. Und auf der Insel ist ein lokaler Umzug schnell und preiswert; für ein paar Dinge löst sogar ein Express-Möbeltransport deinen Tag.",[]),
          ("Grundlegende Formalitäten bei der Ankunft","Parallel bringst du die Formalitäten voran: Anmeldung im Rathaus (Empadronamiento), NIE, falls du noch keine hast, und Versorgungsverträge (Strom, Wasser, Internet). Ein Tipp von Leuten, die es hinter sich haben: Besorg dir so früh wie möglich eine feste Adresse, denn fast alles andere hängt davon ab.",[]),
          ("Einlagerung, während du dich einlebst","Noch kein endgültiges Zuhause oder Renovierung im Gange? Kein Problem. Wir lagern deine Möbel einige Monate sicher ein und bringen sie zurück, sobald du bereit bist. So ziehst du in deinem Tempo um, ohne ein Wohnzimmer voller Kartons.",[])],
  }},
 {"id":"sin-maletas","date":"2026-03-15","rel":["aeropuerto","consigna"],
  "slug":{"es":"viajar-por-mallorca-sin-cargar-maletas","en":"travel-mallorca-without-carrying-luggage","de":"mallorca-ohne-gepaeck-schleppen"},
  "title":{"es":"Viaja por Mallorca sin cargar las maletas | BaggageGo","en":"Travel around Mallorca without carrying your luggage | BaggageGo","de":"Mallorca bereisen, ohne dein Gepäck zu schleppen | BaggageGo"},
  "desc":{"es":"Descubre cómo disfrutar de Mallorca sin arrastrar el equipaje: entrega puerta a puerta, consigna y trucos para viajar ligero desde el aeropuerto.","en":"Discover how to enjoy Mallorca without dragging your bags: door-to-door delivery, storage and tips to travel light from the airport.","de":"Entdecke, wie du Mallorca genießt, ohne dein Gepäck zu schleppen: Lieferung von Tür zu Tür, Aufbewahrung und Tipps zum leichten Reisen."},
  "h1":{"es":"Viaja por Mallorca sin cargar las maletas","en":"Travel around Mallorca without carrying your luggage","de":"Mallorca bereisen, ohne dein Gepäck zu schleppen"},
  "intro":{"es":"Las vacaciones deberían empezar en la playa, no arrastrando maletas por la terminal y el parking. La buena noticia es que en Mallorca puedes moverte con las manos libres de principio a fin. Te contamos cómo.","en":"Holidays should start on the beach, not dragging suitcases through the terminal and the car park. The good news: in Mallorca you can travel hands-free from beginning to end. Here is how.","de":"Urlaub sollte am Strand beginnen, nicht damit, Koffer durch Terminal und Parkplatz zu schleppen. Die gute Nachricht: Auf Mallorca reist du von Anfang bis Ende mit freien Händen. So geht es."},
  "secs":{
    "es":[("Entrega de maletas del aeropuerto al hotel","En cuanto aterrizas, recogemos tu equipaje y lo llevamos directo a tu hotel o villa. Tú sales del aeropuerto ligero y te vas derecho a disfrutar: sin colas en el mostrador de equipajes, sin pelearte con el maletero del coche de alquiler y sin cargar peso bajo el sol.",[]),
          ("Consigna para las horas sin habitación","¿Vuelo de noche y check-out a mediodía? ¿Llegas antes de que la habitación esté lista? Guarda las maletas con nosotros unas horas y exprime ese tiempo de más: un último baño, comer con calma o pasear por el centro sin ir cargado.",[]),
          ("Cambias de hotel sin cargar nada","Y si recorres la isla o haces la Tramuntana cambiando de alojamiento, movemos tu equipaje de un hotel al siguiente mientras tú disfrutas del camino. Viajas ligero cada día y, al llegar, tus cosas ya te están esperando.",[])],
    "en":[("Luggage delivery from the airport to your hotel","The moment you land, we collect your luggage and take it straight to your hotel or villa. You leave the airport light and head off to enjoy yourself, with no queue at the baggage desk, no wrestling with the rental car boot and no lugging weight in the sun.",[]),
          ("Storage for the hours without a room","Night flight but a midday check-out? Arriving before your room is ready? Leave your bags with us for a few hours and make the most of that extra time: one last swim, a slow lunch, or a wander through town without carrying a thing.",[]),
          ("Change hotels without carrying anything","And if you are touring the island or riding the Tramuntana hotel by hotel, we move your luggage to the next one while you enjoy the journey. You travel light every day and, when you arrive, your things are already waiting for you.",[])],
    "de":[("Gepäcklieferung vom Flughafen zum Hotel","Sobald du landest, holen wir dein Gepäck ab und bringen es direkt zu deinem Hotel oder deiner Villa. Du verlässt den Flughafen leicht und gehst gleich genießen: keine Schlange am Gepäckschalter, kein Kampf mit dem Kofferraum des Mietwagens und kein Schleppen in der Sonne.",[]),
          ("Aufbewahrung für die Stunden ohne Zimmer","Nachtflug, aber Check-out am Mittag? Ankunft, bevor das Zimmer fertig ist? Lass dein Gepäck ein paar Stunden bei uns und nutze die Extrazeit: ein letztes Bad, ein entspanntes Mittagessen oder ein Bummel durch die Stadt, ohne etwas zu tragen.",[]),
          ("Wechsle das Hotel, ohne etwas zu tragen","Und wenn du die Insel bereist oder die Tramuntana von Hotel zu Hotel fährst, bringen wir dein Gepäck zum nächsten, während du den Weg genießt. Du reist jeden Tag leicht, und bei der Ankunft warten deine Sachen schon auf dich.",[])],
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
.ctaband{background:linear-gradient(135deg,#081629,#12345E);color:#fff}.ctaband .wrap{text-align:center;padding:52px 22px}.ctaband h2{font-size:1.9rem;font-weight:800;margin-bottom:8px}.ctaband p{color:#d7e3f2;max-width:560px;margin:0 auto 22px}.ctaband .cc{margin-top:20px;font-size:.97rem;color:#c9d6e5}.ctaband .cc a{color:var(--teal);font-weight:600}.ctaband .cc a:hover{color:#E7D4A3}.ctaband .cc span{color:#5f7a99;margin:0 8px}
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
    # Cloudflare Pages sirve URLs limpias (sin .html); canonical/hreflang/sitemap/JSON-LD
    # deben apuntar a la URL limpia para evitar redirects 308 e incoherencias de canonical.
    p = path or ""
    if p.endswith("index.html"):
        p = p[:-len("index.html")]   # index.html -> ""  ·  en/index.html -> en/
    elif p.endswith(".html"):
        p = p[:-5]
    return DOMAIN + "/" + p

def rel(from_path, to_path):
    """URL relativa LIMPIA (sin .html) de from_path a to_path — cero redirects 308 en Cloudflare.
    Respeta anclas #fragment (las separa, limpia la ruta y las vuelve a unir)."""
    frag = ""
    if "#" in to_path:
        to_path, f = to_path.split("#", 1)
        frag = "#" + f
    fd = os.path.dirname(from_path)
    r = os.path.relpath(to_path, fd if fd else ".").replace("\\", "/")
    if r.endswith("index.html"):
        r = r[:-len("index.html")] or "./"   # index.html -> ./ ; ../index.html -> ../
    elif r.endswith(".html"):
        r = r[:-5]
    return r + frag

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
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{DOMAIN}/og-image.png">
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
    return ('{"@context":"https://schema.org","@type":"MovingCompany","@id":"%(d)s/#business",'
            '"name":"%(b)s Mallorca","description":"Entrega de equipaje, transporte y mudanzas en Mallorca",'
            '"url":"%(d)s/","logo":"%(d)s/og-image.png","image":"%(d)s/og-image.png",'
            '"telephone":"%(p)s","email":"%(e)s","priceRange":"€€","currenciesAccepted":"EUR",'
            '"areaServed":{"@type":"AdministrativeArea","name":"Mallorca, Illes Balears"},'
            '"address":{"@type":"PostalAddress","addressLocality":"%(c)s","addressRegion":"Illes Balears","addressCountry":"ES"},'
            '"geo":{"@type":"GeoCoordinates","latitude":39.5696,"longitude":2.6502},'
            '"sameAs":["https://wa.me/%(w)s"]}'
            % {"d":DOMAIN,"b":BRAND,"p":PHONE_DISPLAY,"e":EMAIL,"c":CITY,"w":WA})

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
    lbl = {"es":"o escríbenos directamente","en":"or reach us directly","de":"oder schreib uns direkt"}[lang]
    return f"""<section class="ctaband"><div class="wrap">
<h2>{esc(ui['cta_band_t'])}</h2><p>{esc(ui['cta_band_p'])}</p>
<a href="{contact}" class="btn btn-primary">{esc(ui['cta_main'])}</a>
<div class="cc">{esc(lbl)}: <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {esc(PHONE_DISPLAY)}</a> <span>·</span> <a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div></section>"""

# related services block
def related_services(lang, out_path, exclude=None):
    ui = UI[lang]
    names = {"es":{"aeropuerto":"Entrega desde el aeropuerto","consigna":"Consigna de equipaje","ciclistas":"Equipaje para ciclistas","mudanzas":"Mudanzas exprés","mercancias":"Transporte de mercancías","guardamuebles":"Guardamuebles","bicicletas":"Transporte de bicicletas","portes":"Portes y muebles"},
             "en":{"aeropuerto":"Airport delivery","consigna":"Luggage storage","ciclistas":"Cyclist luggage","mudanzas":"Express moving","mercancias":"Cargo van & goods","guardamuebles":"Storage","bicicletas":"Bike transport","portes":"Man with a van"},
             "de":{"aeropuerto":"Flughafen-Lieferung","consigna":"Gepäckaufbewahrung","ciclistas":"Radfahrer-Gepäck","mudanzas":"Express-Umzüge","mercancias":"Warentransport","guardamuebles":"Einlagerung","bicicletas":"Fahrradtransport","portes":"Möbeltransport"}}[lang]
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
     "es":[("¿Cuánto cuesta la entrega de maletas en "+name+"?","Desde 14 € por dos maletas puerta a puerta en "+name+". El precio depende del número de bultos y del punto exacto; te lo confirmamos al instante por WhatsApp."),
           ("¿Entregáis en "+name+" el mismo día?","Sí. Con reserva anticipada entregamos tu equipaje en "+name+" el mismo día, y también lo recogemos para llevarlo al aeropuerto o a otro alojamiento.")],
     "en":[("How much is luggage delivery in "+name+"?","From €14 for two bags door to door in "+name+". The price depends on the number of items and the exact point; we confirm instantly on WhatsApp."),
           ("Do you deliver in "+name+" the same day?","Yes. With advance booking we deliver your luggage in "+name+" the same day, and we also collect it to take to the airport or another accommodation.")],
     "de":[("Was kostet die Gepäcklieferung in "+name+"?","Ab 14 € für zwei Gepäckstücke von Tür zu Tür in "+name+". Der Preis hängt von der Anzahl der Stücke und dem genauen Ort ab; wir bestätigen sofort per WhatsApp."),
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
             "svc":{"aeropuerto":("Maletas puerta a puerta","Aeropuerto ↔ hotel ↔ villa. Llega con las manos libres."),"consigna":("Consigna de equipaje","Guarda tus maletas por horas antes del check-in o después del check-out."),"ciclistas":("Ciclistas y senderistas","Movemos tu equipaje y tu bici de hotel a hotel por la Tramuntana."),"mudanzas":("BaggageGo Moving","Mudanzas pequeñas y exprés en la isla: rápidas y aseguradas."),"mercancias":("Transporte de mercancías","Furgoneta con conductor para mercancía y envíos voluminosos en toda la isla."),"guardamuebles":("Guardamuebles","Almacenaje seguro por meses, con recogida y entrega a domicilio."),"bicicletas":("Transporte de bicicletas","Del aeropuerto al hotel y entre etapas, para cicloturistas y grupos."),"portes":("Portes y muebles","Muebles sueltos, mini mudanzas y portes urgentes en toda la isla.")},
             "more":"Ver más","ver_zona":"Ver zona"},
       "en":{"title":"BaggageGo Mallorca · Luggage delivery & moving","desc":"Door-to-door luggage delivery in Mallorca: airport, hotels and villas. Service for Tramuntana cyclists, storage and express moving. ES·EN·DE.",
             "eyebrow":"Luggage delivery & moving in Mallorca","h1a":"Your bags","h1b":"travel on their own.",
             "sub":"We pick up your luggage at the airport, hotel or villa and deliver it wherever you are. You just travel light.",
             "book_t":"Get an instant price","book_p":"Luggage from A to B, anywhere on the island.","f_from":"From","f_to":"To","f_bags":"Bags","f_date":"Date",
             "sh_s_e":"What we do","sh_s_t":"Everything moves, so you don't have to","sh_z_e":"Local SEO","sh_z_t":"Luggage delivery by area in Mallorca",
             "svc":{"aeropuerto":("Door-to-door luggage","Airport ↔ hotel ↔ villa. Arrive hands-free."),"consigna":("Luggage storage","Store your bags by the hour before check-in or after check-out."),"ciclistas":("Cyclists & hikers","We move your luggage and bike hotel to hotel across the Tramuntana."),"mudanzas":("BaggageGo Moving","Small, express moves across the island: fast and insured."),"mercancias":("Cargo van & goods","A cargo van with driver for goods and bulky deliveries island-wide."),"guardamuebles":("Storage","Secure monthly storage, with home pick-up and delivery."),"bicicletas":("Bike transport","From airport to hotel and between stages, for cyclists and groups."),"portes":("Man with a van","Single furniture items, small moves and urgent jobs across the island.")},
             "more":"Learn more","ver_zona":"View area"},
       "de":{"title":"BaggageGo Mallorca · Gepäcklieferung & Umzüge","desc":"Gepäcklieferung von Tür zu Tür auf Mallorca: Flughafen, Hotels und Villen. Service für Tramuntana-Radfahrer, Aufbewahrung und Express-Umzüge. ES·EN·DE.",
             "eyebrow":"Gepäcklieferung & Umzüge auf Mallorca","h1a":"Dein Gepäck","h1b":"reist von allein.",
             "sub":"Wir holen dein Gepäck am Flughafen, Hotel oder in der Villa ab und liefern es dorthin, wo du bist. Reise einfach leicht.",
             "book_t":"Sofortpreis erhalten","book_p":"Gepäck von A nach B, überall auf der Insel.","f_from":"Von","f_to":"Nach","f_bags":"Gepäck","f_date":"Datum",
             "sh_s_e":"Was wir tun","sh_s_t":"Alles bewegt sich – nur du nicht","sh_z_e":"Lokales SEO","sh_z_t":"Gepäcklieferung nach Gebiet auf Mallorca",
             "svc":{"aeropuerto":("Gepäck von Tür zu Tür","Flughafen ↔ Hotel ↔ Villa. Komm mit freien Händen an."),"consigna":("Gepäckaufbewahrung","Lagere dein Gepäck stundenweise vor dem Check-in oder nach dem Check-out."),"ciclistas":("Radfahrer & Wanderer","Wir bringen dein Gepäck und dein Rad von Hotel zu Hotel durch die Tramuntana."),"mudanzas":("BaggageGo Moving","Kleine Express-Umzüge auf der Insel: schnell und versichert."),"mercancias":("Warentransport","Transporter mit Fahrer für Waren und sperrige Lieferungen inselweit."),"guardamuebles":("Einlagerung","Sichere monatliche Einlagerung, mit Abholung und Lieferung."),"bicicletas":("Fahrradtransport","Vom Flughafen zum Hotel und zwischen Etappen, für Radfahrer und Gruppen."),"portes":("Möbeltransport","Einzelmöbel, kleine Umzüge und dringende Transporte inselweit.")},
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
    pr={"es":[("Consigna de equipaje","4,90 €","por bulto y día"),("Entrega de maletas","14 €","2 maletas, puerta a puerta"),("Pack Consigna + Entrega","12 €","guardamos y te lo entregamos"),("Transporte de bicicletas","19 €","por bici y día"),("Portes / mini-mudanza","49 €","1ª hora · furgoneta + operario"),("Furgoneta con conductor","59 €","por hora (mín. 2 h)"),("Mudanza exprés","390 €","mini · piso 2 hab. desde 690 €"),("Guardamuebles","69 €","al mes · recogida incluida")],
        "en":[("Luggage storage","4,90 €","per bag and day"),("Luggage delivery","14 €","2 bags, door to door"),("Storage + Delivery pack","12 €","we store and deliver"),("Bike transport","19 €","per bike and day"),("Man with a van","49 €","1st hour · van + helper"),("Cargo van with driver","59 €","per hour (min. 2 h)"),("Express moving","390 €","mini · 2-bed from 690 €"),("Storage","69 €","per month · pick-up included")],
        "de":[("Gepäckaufbewahrung","4,90 €","pro Stück und Tag"),("Gepäcklieferung","14 €","2 Stück, Tür zu Tür"),("Paket Aufbewahrung + Lieferung","12 €","wir lagern und liefern"),("Fahrradtransport","19 €","pro Rad und Tag"),("Möbeltransport","49 €","1. Stunde · Transporter + Helfer"),("Transporter mit Fahrer","59 €","pro Stunde (min. 2 Std.)"),("Express-Umzug","390 €","mini · 2-Zi. ab 690 €"),("Einlagerung","69 €","pro Monat · Abholung inkl.")]}[lang]
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
