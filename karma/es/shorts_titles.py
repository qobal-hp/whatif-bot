"""Sharper Spanish shorts titles (short enough for the Shorts feed). Writes them into the specs and prints the update JSON."""
import json
IDS = {"01": "Xpapn2jBgE4 KmMiBMWfMo4 b_cE0ZKmSiw TMIFYoxTKdw vtBFy-b-F0k",
       "02": "jyT4Txh9G5A LykJwyzts_o 1TakVKVpstE tLQcfBaBKLs qOTVIDLOE4U",
       "03": "kvTI2X5AVVM 0HwBIJGpEJQ ywskihgGzEQ ylQtUHynbI8 L3AQQLjqb50",
       "04": "F2ODumD_vCg 7LHpsKJo_x8 M7UpGewJBzU xxDuisJLh2Q ZEvtMZMdjCs",
       "07": "4MhtJVN9io0 V2N4lRbY8IE RDvyRYMomVg 8cRfNR1lRu4 7zpb__-sJIE",
       "05": "DEKaD_hnNRA 4vF3HtRz_5g 0ZD1_pEUdsI W3J0-y_GzOM xtLpvAHTfUE"}
TITLES = {
 "01": ["Puso los mensajes de su novio en la pantalla de la boda 😳", "Llegó dos días antes… y escuchó todo", "“¡Me dijiste que lo habías borrado!” 💀",
        "El abogado puso el audio frente a 200 invitados", "Él creyó que ella había firmado…"],
 "02": ["Papá le dejó 1 dólar. Sus hermanos se rieron…", "“Si no te dejara nada… ¿me odiarías?”", "“Sal por esa puerta y no vuelvas”… y ella sonrió",
        "Su propio hermano lo traicionó frente al consejo", "Les regaló su herencia: 1 dólar 😏"],
 "03": ["Siguió a su esposo en Nochebuena… 💔", "La otra mujer le dio una carpeta. Adentro estaba SU firma", "“Te amo. Voy a firmar.” Pero no como él pensaba",
        "Sus dos esposas. En la misma sala.", "“Un error es olvidar un aniversario.”"],
 "04": ["“Tiene que creer que lo está perdiendo todo…”", "La echó de la casa en Acción de Gracias 🦃", "La corrieron… y una hora después sonó su teléfono",
        "“¡Yo no falsifiqué nada!” Entonces habló el abogado", "“Esta vez me voy porque yo quiero.”"],
 "07": ["¿Para quién es la silla vacía? 🪑", "40 años sin verse. Solo tenía una pregunta", "Llegó a la cena con un cheque viejo… con SU firma",
        "40 años de cartas. Todas sin abrir.", "“¿Dónde me siento?” 41 años esperando esa pregunta"],
 "05": ["Dijo que su papá estaba muerto… y se abrieron las puertas", "Su suegra le dio el pésame. Su papá está vivo.", "Leyó la página de la boda de su hija: “En memoria de…”",
        "“No puedes probarlo.” “En realidad… sí puedo.”", "Se quitó el anillo en el altar 💍"],
}
changes = []
for ep, ids in IDS.items():
    path = f"karma/es/ep{ep}_es.json"
    spec = json.load(open(path))
    for short, vid, t in zip(spec["shorts"], ids.split(), TITLES[ep]):
        short["youtube_title"] = f"{t} #shorts"
        changes.append({"id": vid, "title": short["youtube_title"]})
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=1)
print(json.dumps(changes, ensure_ascii=False))
