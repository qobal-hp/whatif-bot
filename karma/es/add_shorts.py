"""Add five Spanish shorts to each Spanish episode spec (karma/es/ep0N_es.json)."""
import json

LINKS = {"ep01": "lXJawSajgBg", "ep02": "-Ew-ROqtSC4", "ep03": "At_bwIfa4W4",
         "ep04": "3S6OU8JEl-Q", "ep05": "OH9xYM5f1Bk", "ep07": "jtvhz0uVMWk"}
TAGS = {"ep01": "#boda", "ep02": "#herencia", "ep03": "#familiasecreta", "ep04": "#acciondegracias",
        "ep05": "#boda", "ep07": "#acciondegracias"}

# (from, to, on-screen title, YouTube title)
SHORTS = {
    "ep01": [
        ("s04", "s16", "La novia tenía una sorpresa|para toda la boda", "Puso los mensajes secretos de su prometido en su propia boda"),
        ("s23", "s26", "Volvió a casa|dos días antes", "Regresó antes de su viaje y escuchó voces en la recámara"),
        ("s60", "s65", "\"¡Me dijiste que|lo habías borrado!\"", "Él creyó que ella había borrado los mensajes. No lo hizo."),
        ("s69", "s72", "\"Ponle el resto|del mensaje de voz.\"", "El abogado pidió una sola cosa frente a 200 invitados"),
        ("s91", "s94", "Él creyó que ella firmó.|No firmó.", "Se casó con ella por su dinero. Ella le llevaba 19 días de ventaja."),
    ],
    "ep02": [
        ("s09", "s19", "Sus hermanos: 12 millones.|Ella: un dólar.", "Se rieron cuando papá le dejó un dólar. Entonces el abogado siguió leyendo."),
        ("s34", "s37", "\"Si no te dejara nada...|¿me odiarías?\"", "Su papá le hizo una pregunta extraña seis meses antes de morir"),
        ("s89", "s95", "\"Sal por esa puerta|y no vuelvas.\"", "Su hermano le dio un ultimátum en la cena. Ella sonrió."),
        ("s98", "s105", "Traicionó a su hermano|frente al consejo", "Robó 800 mil dólares de la empresa de su papá. Su hermano tenía los correos."),
        ("s106", "s113", "\"Mi herencia.|Es suya. Toda.\"", "Les dio a sus hermanos toda su herencia: un dólar"),
    ],
    "ep03": [
        ("s01", "s15", "Lo siguió|en Nochebuena", "Siguió a su esposo en Nochebuena. Entonces la otra mujer le escribió."),
        ("s39", "s46", "\"Quiero que le creas|a los papeles.\"", "La otra mujer le dio una carpeta. Adentro estaba su firma."),
        ("s79", "s84", "\"Te amo.|Voy a firmar.\"", "Ella aceptó firmar el préstamo. Con una condición."),
        ("s88", "s95", "Sus dos esposas.|Una sola sala.", "Llevó a su esposa al banco a firmar. Entonces entró su otra esposa."),
        ("s96", "s101", "\"Un error es olvidar|un aniversario.\"", "Él dijo que cometió errores. Ella tenía la respuesta perfecta."),
    ],
    "ep04": [
        ("s17", "s29", "\"Tiene que creer que|lo está perdiendo todo.\"", "Madre e hijo planeaban algo para Acción de Gracias. Su hermana los escuchó."),
        ("s41", "s54", "La echó de la casa|en Acción de Gracias", "Echó a su nuera en Acción de Gracias. Entonces ella hizo una pregunta."),
        ("s55", "s61", "Una llamada|desde la gasolinera", "La corrieron en Acción de Gracias. Una hora después sonó su teléfono."),
        ("s105", "s112", "\"¡Yo no falsifiqué nada!\"", "Juró que no falsificó nada. Entonces el abogado habló."),
        ("s120", "s127", "\"Esta vez me voy|porque yo quiero.\"", "Le dijo que se fuera en Acción de Gracias. Y se fue."),
    ],
    "ep05": [
        ("s01", "s11", "Su padre estaba muerto.|Entonces se abrieron las puertas.", "Dijo a todos que su padre había muerto. Entonces entró a su boda."),
        ("s48", "s56", "\"Ethan me dijo|que falleció.\"", "Su suegra le dio el pésame por su papá. Su papá está vivo."),
        ("s80", "s89", "\"En memoria de...\"", "Un mecánico leyó la página de la boda de su hija. Su nombre estaba ahí."),
        ("s133", "s140", "\"No puedes probarlo.\"|\"En realidad... sí puedo.\"", "El novio dijo que nadie podía probarlo. La dama de honor le dio play."),
        ("s161", "s171", "\"No me puedo casar contigo.\"", "Se quitó el anillo en el altar. Luego le pidió algo a su papá."),
    ],
    "ep07": [
        ("s02", "s16", "\"¿Para quién es|la silla de más?\"", "La abuela puso un plato de más en Acción de Gracias. Entonces sonó el timbre."),
        ("s47", "s56", "\"Creí que nunca|me quisiste.\"", "Se vieron por primera vez en 40 años. Ella solo tenía una pregunta."),
        ("s114", "s123", "\"¿Reconoce esto?\"", "Llevó un cheque viejo a la cena de Acción de Gracias. Tenía su firma."),
        ("s133", "s138", "40 años de cartas.|Todas sin abrir.", "Le escribió a su hija cada año. Alguien guardó todas las cartas."),
        ("s198", "s205", "\"¿Dónde me siento?\"", "Guardó esa silla durante 41 años. Por fin su hija se sentó en ella."),
    ],
}

for ep, shorts in SHORTS.items():
    path = f"karma/es/{ep}_es.json"
    spec = json.load(open(path))
    spec["shorts_end_card"] = "Mira la historia completa|en nuestro canal"
    spec["shorts"] = [{"id": f"short{i}", "from": a, "to": b, "title": t, "youtube_title": f"{y} #shorts"}
                      for i, (a, b, t, y) in enumerate(shorts, 1)]
    spec["youtube"]["shorts_description"] = (
        f"Mira la historia completa en Karma Tales en Español: https://youtu.be/{LINKS[ep]}\n"
        f"{spec['youtube']['title']}\n\n#shorts #karmatales #historiasdevenganza {TAGS[ep]}")
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=1)
    print(ep, [s["id"] for s in spec["shorts"]])
