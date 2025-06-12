# Cloud Solar Risk index (CSRI)
# Verdunklungsrisiko-Bewertung für PV-Anlagen
# mit Hilfe der DWD Integration HACS 
(https://github.com/FL550/dwd_weather)

# 

## Einleitung
In der heutigen Zeit gewinnt der Ausbau erneuerbarer Energien stetig an Bedeutung. Insbesondere Photovoltaikanlagen (PV) und Wärmepumpen (WP) spielen eine zentrale Rolle in der energieeffizienten Hausautomation.  
Dieses Projekt verfolgt das Ziel, Verbraucher intelligent zu steuern – und zwar **nicht allein basierend auf aktuellen Einspeisungswerten**, sondern durch die Kombination mehrerer meteorologischer Parameter, die eine **"Verdunklungsgefahr"** berechnen. 

# Cloud Solar Risk Index (CSRI)

![CSRI Badge](https://img.shields.io/badge/CSRI-0--100%25-blue)

**Deutsch:** Wolken-Solar-Risikoindex  
**Kurz:** CSRI  

> Ein dimensionsloser Wert (0 – 100 %), der **die Wahrscheinlichkeit** angibt,  
> mit der die aktuelle solare Einstrahlung (UV-Index + Globalstrahlung in W/m²)  
> durch herannahende Wolken kurzfristig gemindert wird.

## 📊 Warum CSRI ?

Statt nur den momentanen Strahlungswert zu betrachten, bewertet der CSRI die **Dynamik** von UV-Index, Globalstrahlung und Wolkenzug – trianguliert  
aus mehreren DWD-Stationen im 20–30 km-Radius. So entsteht ein Prozentwert, der sowohl PV-Betreibern als auch Sonnenanbetern hilft, drohende Abschattungen vorauszusehen.

Anhand dieser Kennzahl wird dann entschieden, ob die energiehungrige Verbraucher aktiviert werden sollen, um ausschließlich bei günstigen Solarbedingungen den Haushalt zu unterstützen.  

## Herausforderung
Die zentrale Herausforderung besteht darin, ein System zu entwickeln, das:
- **Kurzfristige Wetterveränderungen** (wie variable Bewölkung, wechselnde Windrichtung) realistisch abbildet.
- **Daten von mehreren Wetterstationen** (Giessen, Bad Nauheim, Waldems-Reinborn) integriert, um lokale Schwankungen auszubalancieren.
- **Saisonale Unterschiede** berücksichtigt, denn im Winter sind die Sonneneinstrahlungswerte naturgemäß niedriger als im Sommer.
- **Unplausible oder fehlende Sensordaten** (zum Beispiel ein statischer UV-Index, der nur einmal täglich aktualisiert wird oder fehlende Werte bei Waldems) erkennt und entsprechend behandelt.
- **Dynamisch** und **robust** genug ist, um im täglichen Betrieb verlässliche Entscheidungen zu ermöglichen, ohne dass kurzfristige Störungen oder Messfehler zu unsachgemäßen WP-Aktivierungen führen.

Aus all diesen Gründen stellt die Entwicklung einer fundierten Berechnungslogik für die Risikoermittlung eine anspruchsvolle, aber praxisrelevante Aufgabe dar.

## Projektziel
Das Hauptziel des Projekts ist es, eine **automatische und zuverlässige Berechnung** des Cloud-Solar-Risk Index zu erlangen, welche als Entscheidungsgrundlage für die Automation / Aktivierung dient. Konkret soll das System:

- **Nur Wettereinflüsse berücksichtigen**, die tatsächlich relevant sind, indem eine dynamische Standortgewichtung zum Einsatz kommt.
- Einen **Saisonfaktor** implementieren, der den jahreszeitlichen Verlauf der Sonneneinstrahlung realistisch abbildet.
- **Fehlerhafte oder unvollständige Sensordaten** erkennen und mittels Standardwerten oder neutralen Einflüssen ausgleichen, sodass die Endberechnung nicht verzerrt wird.
- Eine Entscheidung (zum Beispiel "JA", "MODERAT" oder "NEIN") ausgeben, die signifikante Unterschiede in den Wetterbedingungen klar identifiziert und als Automationsbasis in Home Assistant dient.

Der CSRI kann somit in jeder Automation als Bedingung implementiert werden. Die Skala 0% - 100% ermöglicht, individuelle Einstufungen zu verwenden. 

## Hintergrundinformationen und Systemarchitektur

### Wetterstationen und Datenerfassung
Für die Berechnung werden Daten von drei geografisch verteilten Wetterstationen herangezogen:
- **Giessen** (ca. 20 km nördlich des Einspeisepunktes)
- **Bad Nauheim** (ca. 20 km südlich des Einspeisepunktes)
- **Waldems-Reinborn** (ca. 30 km westlich des Einspeisepunktes)

Diese Stationen liefern folgende Messwerte:
- **Bewölkungsgrad:** Gibt an, wie viel Prozent des Himmels von Wolken bedeckt sind.  
- **Windgeschwindigkeit und -richtung:** Entscheidend dafür, ob Wolken in die Richtung des Einspeisepunktes getrieben werden.  
- **UV-Index:** Als Indikator für die Intensität der direkten Sonneneinstrahlung, wenngleich dieser Wert häufig statisch bleibt.
- **Sichtweite:** Richtet sich danach, wie klar die Atmosphäre ist – ein hoher Wert deutet auf klare Verhältnisse hin.

Die Daten werden über die DWD-Integration (und lokale Sensoren) abgerufen, was es ermöglicht, Echtzeitinformationen zu verarbeiten.

### Dynamische Standortgewichtung
Ein wesentlicher Bestandteil der Berechnungslogik ist die dynamische Gewichtung der einzelnen Wetterstationen.  
Hierbei wird ein **vektorbasierter Ansatz** genutzt:
- **Berechnung geografischer Vektoren:** Für jeden Standort wird ein Vektor gebildet, der dessen relative Position zum zentralen Einspeisepunkt (z. B. Oberkleen) beschreibt.  
- **Windvektor:** Die aktuelle Windrichtung wird ebenfalls als Vektor interpretiert.
- **Dot-Produkt:** Das Ergebnis des Dot-Produkts zwischen dem Standortvektor und dem Windvektor liefert einen Wert, der angibt, inwieweit der Standort aktuell relevante Daten liefert. Ein Wert nahe 1 zeigt eine ideale Ausrichtung, während negative oder null Werte bedeuten, dass der jeweilige Standort von den aktuellen Windverhältnissen nicht beeinflusst wird.

Dieser Ansatz reduziert die Auswirkung von Messwerten aus Standorten, die momentan keinen Einfluss auf den Einspeisepunkt haben.

### Saisonaler Faktor und weitere Einflussgrößen
Um den jahreszeitlichen Einfluss zu berücksichtigen, wird eine **Sinusfunktion** verwendet.  
- **Saisonaler Verlauf:** Durch die Verwendung des Tages im Jahr wird ein Faktor ermittelt, der den natürlichen Verlauf der Sonneneinstrahlung – von gering im Winter bis hoch im Sommer – abbildet.
  
Weitere Faktoren, die in die Berechnung einfließen:
- **UV-Index:** Dient als grober Indikator für direkte Sonneneinstrahlung.  
- **Sichtweite:** Wird als Bonusfaktor eingerechnet (z. B. 1.1 bei sehr klaren Bedingungen, 0.9 bei schlechter Sicht).  
- **Bewölkungsgrad:** Direkter Einfluss auf die Solarleistung, da hohe Bewölkung den Ertrag reduziert.

Die Gewichtung der einzelnen Faktoren erfolgt mittels Multiplikation, sodass ein hoher Einfluss (z. B. geringe Bewölkung und günstige Windrichtung) zu einem niedrigeren, also günstigeren WP-Wert führt.

## Details der Berechnung

### 1. Berechnung einzelner Standortwerte
Für jeden Wetterstandort werden die folgenden Schritte durchgeführt:
1. **Validierung der Eingangsdaten:**  
   Jeder gemessene Parameter (z. B. Bewölkungsgrad, Windgeschwindigkeit) wird auf Plausibilität geprüft. Werte, die außerhalb definierter Grenzen liegen, werden durch Standardwerte ersetzt (z. B. 50 % bei Bewölkung).

2. **Anpassung der Einflussfaktoren:**  
   - **Bewölkung:** Hohe Werte wirken sich negativ aus.
   - **Sichtweite:** Ein Bonusfaktor wird zwischen 0.9 und 1.1 verwendet.
   - **UV-Index:** Da dieser häufig statisch bleibt, wird sein Einfluss moderat gewichtet.

3. **Dynamische Windgewichtung:**  
   Mittels vorhin beschriebener Vektorberechnung wird überprüft, ob der Standort laut Windrichtung relevant ist. Nur bei günstiger Ausrichtung wird der volle Einfluss übernommen, ansonsten eine Reduzierung (Faktor 0.9).

### 2. Zusammenführung der Standortwerte
Alle ermittelten Werte der Standorte (Giessen, Bad Nauheim und Waldems) werden zu einem **gewichteten Durchschnitt** zusammengeführt.  
- **Gewichtung durch Vektor-Dot-Produkte:** Die einzelnen Standortwerte werden proportional zum Einflussfaktor (basierend auf der aktuellen Windrichtung) gemittelt.
- **Saisonaler Faktor:** Zum Endergebnis wird abschließend noch ein saisonaler Faktor multipliziert, um jahreszeitliche Unterschiede zu berücksichtigen.

### 3. Entscheidungskriterium für die Einschätzung 
Auf Basis des final berechneten CSRI wird die Empfehlung als Text eingeordnet:
- **JA – Solarbedingungen günstig:** Liegt der Wert unter einem definierten Schwellenwert (z. B. < 40 %), ist ein guter Solarertrag wahrscheinlich.
- **MODERAT – Bedingt empfehlenswert:** Mittlere Werte (z. B. zwischen 40 % und 70 %) deuten auf teilweise günstige Bedingungen hin.
- **NEIN – Solarbedingungen ungünstig:** Hohe Werte (> 70 %) signalisieren, dass die Solarbedingungen nicht ausreichend sind.
  
Zusätzlich wird eine **Unsicherheitsprüfung** der Winddaten durchgeführt. Weichen die Windrichtungen der verschiedenen Stationen um mehr als eine definierte Toleranz ab (z. B. 30°), wird der finale WP-Wert um einen fixen Betrag +5% erhöht und als unsicher markiert.

## Praxisnähe und Realitätsbezug
Die vorliegende Berechnung basiert auf **realen Wetter- und Einspeisedaten** und ist darauf ausgelegt, sich dynamisch an kurzfristige Wetteränderungen anzupassen.  
- **Geografische Lage:** Mehrere Standorte aus der Region werden herangezogen, sodass lokale Besonderheiten und Wetterphänomene realistisch abgebildet werden.
- **Dynamische Gewichtung:** Durch die vektorbasierte Analyse wird sichergestellt, dass nur tatsächlich relevante Daten den WP-Wert beeinflussen.
- **Saisonaler Faktor:** Mit der Sinusfunktion wird ein realistischer zeitlicher Verlauf geschaffen, der zwischen Sommer und Winter differenziert.
- **Robuste Validierung:** Ungültige oder fehlende Daten werden erkannt und durch Standardwerte oder neutrale Einflüsse kompensiert. Dadurch wird vermieden, dass Ausreißer oder Messfehler das Gesamtergebnis massiv verfälschen.
  
Diese Methode liefert **praxisnahe und zuverlässige Werte**, die als solide Grundlage für die Bewertung dienen. Der Berechnungsansatz wurde so konzipiert, dass er in unterschiedlichen Witterungslagen robust reagiert und bei kritischen Winkeln (z. B. starke Windabweichungen) entsprechende Anpassungen vornimmt.

## Installation & Nutzung
1. **Setup in Home Assistant:**  
   Integriere die YAML-Konfiguration in Dein Home Assistant Setup, idealerweise als eigene `solarbewertung.yaml`.
2. **Anpassung der Sensoren:**  
   Stelle sicher, dass alle verwendeten Sensoren (für Bewölkung, Wind, UV, Sicht etc.) korrekt in HA eingebunden und benannt sind.
3. **Erstellung von Automationen:**  
   Verwende den berechneten CSRI und die entsprechende Entscheidung als Trigger für Automationen, etwa um die Verbraucher zu aktivieren oder zu deaktivieren.
4. **Monitoring & Debugging:**  
   Überprüfe regelmäßig die Zustände der Sensoren und der berechneten Werte über die Home Assistant Developer Tools, um sicherzustellen, dass die Daten valide und die Berechnungen korrekt sind.

## Lizenz
Dieses Projekt steht unter der **MIT-Lizenz**. Nutzung, Anpassung und Weitergabe sind frei möglich, solange die Lizenzbedingungen beachtet werden.

## Ausblick
Zukünftige Erweiterungen könnten beinhalten:
- **Dynamischere UV-Datenquellen**, um kurzfristige Änderungen besser abzubilden.
- **Integration zusätzlicher Wetterstationen** oder lokaler Sensoren.
- **Feinjustierung der Gewichtungsfaktoren** anhand von Praxistests und Langzeitdaten.
- **Erweiterte Visualisierungen** in Home Assistant, um die wichtigsten Parameter und Entscheidungsgrundlagen transparenter darzustellen.

---

Diese ausführliche Dokumentation vermittelt einen tiefen Einblick in den Berechnungsprozess und die eingesetzten Methodiken. Sie zeigt auf, wie praxisnahe und realistische Werte erzielt werden können, um die Wärmepumpensteuerung optimal zu unterstützen.



# WP Solarbewertung – Dynamische Steuerung der Wärmepumpe basierend auf Wetter- und PV-Daten

## Einleitung
In Zeiten steigender Energiekosten und wachsender Anforderungen an die Energieeffizienz gewinnt die intelligente Steuerung von Haushaltsgeräten immer mehr an Bedeutung.  
Dieses Projekt hat sich der Optimierung der elektrischen Verbraucher verschrieben, indem es eine Kennzahl, den „Cloud-Solar-Risk Index", berechnet. Diese Kennzahl dient als Entscheidungsgrundlage dafür, wann die Verbraucher eingeschaltet werden können – und zwar basierend auf den gegenwärtigen und prognostizierten Wetterbedingungen, die den PV-Ertrag maßgeblich beeinflussen.

Die Kombination von **wetterbasierten Parametern** und **geografisch gewichteter Datenfusion** soll sicherstellen, dass die Wärmepumpe speziell dann aktiv ist, wenn ausreichend Solarenergie zur Verfügung steht. So wird der Netzstrombezug minimiert und die Effizienz des gesamten Systems maximiert.

---

## Herausforderung
In der Praxis treten bei der Steuerung einer WP zahlreiche Herausforderungen auf:

- **Kurzfristige Wetteränderungen:**  
  Die Wetterbedingungen (z. B. Bewölkung, Windrichtung) ändern sich häufig und können kurzfristig den Ertrag aus Photovoltaik-Anlagen beeinflussen. Ein statischer Ansatz reicht hier nicht aus.

- **Unterschiedliche Datenquellen:**  
  Die verwendeten Wetterdaten stammen aus mehreren Quellen (Giessen, Bad Nauheim, Waldems-Reinborn). Unterschiede in Messwerten und Updateintervallen (z. B. UV-Index, der nur einmal täglich vorausgesagt wird) erschweren eine einheitliche Bewertung.

- **Lokale Besonderheiten:**  
  Aufgrund geografischer Unterschiede liefert jede Wetterstation teilweise unterschiedliche Daten – was bedeutet, dass ein einzelner Messwert allein nicht repräsentativ für den gesamten Anlagenbetrieb ist.

- **Saisonale Schwankungen:**  
  Die Sonneneinstrahlung variiert stark im Jahresverlauf. Ein System, das beispielsweise im Sommer zu oft aktiviert wird, muss im Winter restriktiver arbeiten, um Fehlauslösungen zu vermeiden.

- **Messunsicherheiten und Ausreißer:**  
  Sensoren können fehlerhafte oder unvollständige Werte zurückliefern. Eine robuste Validierung dieser Eingangsdaten ist daher zwingend erforderlich, um Fehlentscheidungen zu verhindern.

Dieses Projekt adressiert alle genannten Herausforderungen durch einen mehrstufigen, dynamischen Ansatz, der alle relevanten meteorologischen Faktoren intelligent kombiniert.

---

## Zielsetzung
Das primäre Ziel des Projekts ist es, eine **zuverlässige und automatisierte Berechnung** des Cloud-Solar-Risk Index zu implementieren, die folgendes ermöglicht:

- **Dynamische Datennutzung:**  
  Es werden mehrere, direkt verfügbare Wetterparameter in Echtzeit verarbeitet, sodass stets aktuelle Bedingungen in die Entscheidungsfindung einfließen.

- **Geografisch gewichtete Integration:**  
  Mittels eines vektorbasierten Ansatzes wird ermittelt, welche Wetterstationen gerade einen relevanten Einfluss haben. Dadurch wird verhindert, dass einzelne Outlier allein das System dominieren.

- **Saisonale Differenzierung:**  
  Durch die Einbindung eines sinusbasierten saisonalen Faktors werden langfristige Trends (somit Winter vs. Sommer) realistisch abgebildet.

- **Fehlerrobustheit:**  
  Unplausible oder fehlende Daten werden erkannt und neutralisiert, um das System stabil zu halten. Beispielsweise werden bei fehlenden Waldems-Daten neutrale Einflüsse genutzt, sodass diese Wetterstation das Gesamtergebnis nicht verzerrt.

- **Klare Entscheidungsgrundlage:**  
  Basierend auf der berechneten Kennzahl wird eine eindeutige Empfehlung („JA –“, „MODERAT –“, „NEIN –“) generiert, die als Trigger in der Home Assistant-Automation eingesetzt wird.

---

## Hintergrundinformationen

### Datengrundlage und Wetterstationen
Die Berechnungen basieren auf Messwerten von **drei regionalen Wetterstationen**:

- **Giessen:**  
  Liegt ca. 20 km nördlich des zentralen Einspeisepunktes. Typische Messwerte umfassen Bewölkungsgrad, Windgeschwindigkeit, Windrichtung, UV-Index und Sichtweite.

- **Bad Nauheim:**  
  Befindet sich ca. 20 km südlich. Hier spiegeln die Messwerte einen ähnlichen, aber lokal angepassten Wettertrend wider.

- **Waldems-Reinborn:**  
  Diese Station befindet sich ca. 30 km westlich. Aufgrund technischer Einschränkungen oder Datenlücken (z. B. unsicherer Sonneneinstrahlungswert) wird hier eine neutralere Gewichtung vorgenommen, damit unplausible Werte den Gesamtwert nicht verfälschen.

### Erklärung der Parameter

- **Bewölkungsgrad:**  
  Dieser Wert gibt an, wie groß der Wolkenanteil am Himmel ist. Er ist ein kritischer Faktor, da Wolken die direkte Sonneneinstrahlung blockieren und somit den PV-Ertrag verringern.

- **Windgeschwindigkeit und -richtung:**  
  Wind beeinflusst die Bewegung der Wolken. Eine günstige Windrichtung kann bedeuten, dass wolkenreiche Bereiche weggeweht werden, sodass die Sonne länger ungestört scheint. Ein vektorbasiertes Modell berechnet, ob ein Standort im Einflussbereich des aktuellen Windes liegt.

- **UV-Index:**  
  Der UV-Index liefert einen groben Anhaltspunkt über die Intensität der Sonneneinstrahlung. Obwohl er meist nur einmal täglich aktualisiert wird, fließt er als ergänzender Faktor in die Berechnung ein.

- **Sichtweite:**  
  Eine hohe Sichtweite deutet auf klare atmosphärische Bedingungen hin, während eine schlechte Sichtweite auf einen hohen Schleier von Wolken oder Dunst hindeutet. Dies wird als Bonusfaktor eingerechnet.

- **Saisonaler Faktor:**  
  Über eine Sinusfunktion wird ein Faktor berechnet, der den natürlichen, jahreszeitlichen Verlauf der Sonneneinstrahlung abbildet – niedriger im Winter, höher im Sommer.

---

## Methodik und Berechnungsdetail

### 1. Validierung der Eingangsdaten
Für jeden Standort werden die gemessenen Werte vor der Berechnung validiert:
- **Bereichsprüfungen:**  
  Werte wie der Bewölkungsgrad (0–100 %) oder die Windgeschwindigkeit (0–60 m/s) werden überprüft. Werte außerhalb des plausiblen Bereichs werden durch Standardwerte ersetzt (z. B. 50 % für Bewölkung).

- **Fehlerbehandlung:**  
  Falls Sensordaten fehlen oder als „unbekannt“ zurückgegeben werden, greift eine Fallback-Logik. Zum Beispiel werden bei Waldems fehlende Werte neutral behandelt, sodass diese Station keinen verzerrenden Einfluss auf die Berechnung hat.

### 2. Einzelberechnung der Standort-Solarwahrscheinlichkeit
Jeder Standort (Giessen, Bad Nauheim, Waldems) wird folgendermassen verarbeitet:
- **Parameterintegration:**  
  Jeder Messwert (Bewölkung, Wind, UV, Sicht) fließt mit einem bestimmten Faktor in die Berechnung ein:
  - Bewölkung wirkt invers proportional zur Solarwahrscheinlichkeit.
  - UV-Werte werden skaliert (z. B. von 0.8 bis 1.2) und tragen positiv bei, wenn sie höher sind.
  - Sichtweite wird als Bonus (zwischen 0.9 und 1.1) eingerechnet.
- **Windgewichtung:**  
  Mittels eines vektorbasierten Ansatzes wird der Einfluss der Windrichtung ermittelt. Standorte, deren Richtungen mit dem aktuellen Wind übereinstimmen, erhalten eine höhere Gewichtung (Faktor 1), während andere leicht reduziert werden (Faktor 0.9).

### 3. Zusammenführung der Daten mittels Vektoranalyse
- **Geografische Vektorberechnung:**  
  Für jeden Standort wird ein Vektor basierend auf seiner geografischen Lage im Verhältnis zum zentralen Einspeisepunkt berechnet. Dabei werden die Differenzen in Längengrad und Breitengrad unter Berücksichtigung der Erdkrümmung (Umrechnung in Kilometer) genutzt.
- **Bestimmung des relevanten Einflusses:**  
  Die aktuellen Windrichtung wird in einen Vektor umgerechnet. Anhand des Dot-Produkts der Standortvektoren mit dem Windvektor wird der Relevanzfaktor (zwischen 0 und 1) bestimmt – er zeigt, wie gut der jeweilige Standort in den aktuellen Windfluss eingebunden ist.
- **Gewichteter Durchschnitt:**  
  Die Einzelwerte der einzelnen Standorte werden entsprechend ihres Einflussfaktors zu einem Gesamt-WP-Wert gemittelt. Sollte der Gesamtwert zu unsicher erscheinen (etwa bei starken Differenzen in der Windrichtung), wird eine Korrektur vorgenommen.

### 4. Saisonaler Faktor
Ein saisonal angepasster Korrekturfaktor, der über eine Sinusfunktion berechnet wird, wird zum endgültigen WP-Wert hinzugefügt.  
- **Mathematische Herleitung:**  
  Der Tag im Jahr (als Tag der Jahres) wird in einen Winkel umgerechnet, der in die Sinusfunktion eingeht, sodass ein Wert zwischen 0 und 1 entsteht. Dieser Faktor passt den WP-Wert an, sodass im Winter (bei geringerer Sonneneinstrahlung) die WP seltener aktiviert wird als im Sommer.

### 5. Entscheidungslogik der Wärmepumpe
Nach der Berechnung des CSRI erfolgt die Entscheidungsfindung:
- **Schwellwerte:**  
  Der finale WP-Wert wird mit vordefinierten Schwellen verglichen:
  - **Wert < 40 %:** Sehr günstige Bedingungen – WP wird aktiviert („JA –“).
  - **Wert zwischen 40 % und 70 %:** Bedingt empfehlenswerte Bedingungen – WP wird moderat aktiv („MODERAT –“).
  - **Wert > 70 %:** Ungeeignete Bedingungen – WP bleibt inaktiv („NEIN –“).
- **Unsicherheitskennzeichnung:**  
  Zusätzlich wird eine Prüfung der Konsistenz der Winddaten durchgeführt; wenn die Windrichtungen der Standorte zu sehr auseinander liegen (z. B. Differenz > 30°), wird der WP-Wert leicht heraufgesetzt (+5) und als „unsicher“ markiert. Dies warnt vor instabilen oder uneinheitlichen Wetterbedingungen.

---

## Realitätsbezug und Praxisnähe

### Datenbasis und Aktualität
- **Live-Wetterdaten:**  
  Die Berechnung basiert auf Echtzeitmessungen mehrerer Wetterstationen, was den Ansatz sehr aktuell macht.
- **Regionale Differenzierung:**  
  Durch den Einsatz von drei unterschiedlichen Standorten wird eine regionale Abdeckung erzielt, sodass lokale Besonderheiten erfasst werden.
- **Robuste Validierung:**  
  Durch automatische Fallback-Mechanismen und Standardwerte wird ein hoher Grad an Stabilität gewährleistet – selbst wenn einzelne Sensoren fehlerhafte oder fehlende Werte liefern.

### Dynamische und flexible Gewichtung
- **Vektoranalyse:**  
  Der Einsatz eines vektor-basierten Modells für die Windgewichtung sorgt für eine dynamische Anpassung: Nur tatsächlich relevante Daten werden bei der Entscheidung berücksichtigt.
- **Saisonale Anpassung:**  
  Die Sinusfunktion, die den saisonalen Verlauf abbildet, sorgt dafür, dass sich der WP-Wert über das Jahr hinweg realistisch verändert. Dies spiegelt den tatsächlichen Verlauf der Sonnenstunden und PV-Erträge wider.

### Praxisnähe
- **Automatisierung:**  
  Der berechnete CSRI dient als Grundlage, um Automatisierungen in Home Assistant zu triggern. Dies führt zu einer reaktionsschnellen und energieeffizienten Steuerung der Verbraucher.
- **Robustheit:**  
  Der mehrstufige Validierungsprozess und die dynamische Gewichtung minimieren die Gefahr von Fehlentscheidungen durch einmalige Ausreißer oder unplausible Sensordaten.
- **Energieeffizienz:**  
  Durch den intelligenten Einsatz der WP entsprechend der tatsächlichen Solarbedingungen wird der Netzstrombezug minimiert, was zu einer potenziellen Kostensenkung und einer effizienteren Nutzung der eigenen PV-Anlage führt.

---

## Installation & Nutzung

1. **Voraussetzungen:**  
   - Home Assistant ist installiert und läuft.
   - Alle benötigten Sensoren (Bewölkungsgrad, Windgeschwindigkeit, Windrichtung, UV-Index, Sichtweite) sind eingebunden und liefern Daten.

2. **Integration:**  
   - Speichere die YAML-Datei (z. B. als `solarbewertung.yaml`) im entsprechenden Verzeichnis Deiner Home Assistant Konfiguration.
   - Binde die YAML-Datei in Dein HA-Setup ein (über `configuration.yaml` oder entsprechende Splits).

3. **Automatisierungen:**  
   - Erstelle Automationen, die auf Basis des berechneten CSRI (und der daraus resultierenden Entscheidung) die Verbraucher zu schalten.
   - Kombiniere hierzu vorhandene Einspeisedaten deiner PV-Anlage oder Zeitfenster. Der CSRI erkennt nicht die momentane Leistung deiner PV.
   - Nutze zusätzlich die detailreiche Entscheidungsbegründung als Information zur Fehlerdiagnose und Optimierung.

4. **Monitoring:**  
   - Über die Developer Tools in Home Assistant können die Zustände und berechneten Werte kontrolliert werden, um sicherzustellen, dass die Sensoren korrekt liefern und die Berechnungen wie erwartet funktionieren.

---

## Ausblick und Weiterentwicklung

Zukünftige Erweiterungen dieses Projekts könnten beinhalten:
- **Integration dynamischerer UV-Daten:**  
  Eine alternative Datenquelle für den UV-Index, die stündlich aktualisiert wird, könnte zur weiteren Verbesserung der Genauigkeit beitragen.
- **Erweiterte Sensorfusion:**  
  Zusätzliche lokale Sensoren oder noch mehr regionale Wetterstationen könnten integriert werden, um den geografischen Einfluss noch feiner abbilden zu können.
- **Optimierung der Gewichtung:**  
  Durch Langzeitanalysen und Praxistests können die Gewichtungsfaktoren weiter optimiert und an die individuellen Gegebenheiten angepasst werden.
- **Visualisierung:**  
  Eine übersichtliche Darstellung der wichtigsten Parameter und Berechnungsresultate in Home Assistant ermöglicht eine noch bessere Nachvollziehbarkeit und Diagnose der WP-Steuerung.
- **Machine Learning:**  
  Mittelfristig könnte ein lernender Algorithmus implementiert werden, der auf historischen Daten basiert und die Entscheidung noch weiter verfeinert.

---

## Lizenz
Dieses Projekt steht unter der **MIT-Lizenz**. Jeder darf den Code nutzen, anpassen und weitergeben, solange die Bedingungen der Lizenz eingehalten werden.

---

## Zusammenfassung
Dieses Projekt präsentiert einen **robusten, dynamischen** und **praxisnahen Ansatz** zur Steuerung elektrischer Verbraucher (z.B. Wärmepumpe / Waschmaschine usw.), basierend auf einer fundierten Berechnung der möglichen Einschränkung der Sonneneinstrehlund durch Wolkenbewegungen. Durch den Einsatz mehrerer Wetterstationen, einer intelligenten vektorbasierten Gewichtung und der Berücksichtigung von saisonalen Einflüssen wird ein zuverlässiges System geschaffen, das die Automation von elektrischen Verbrauchern optimiert und dabei hilft, erneuerbare Energien effizienter zu nutzen.

---

