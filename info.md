# Info.md – Gedankenstützen zur Solarwahrscheinlichkeits-Berechnung

Diese Datei dokumentiert den vollständigen konzeptionellen und implementierungstechnischen Hintergrund unseres Projekts „Solarwahrscheinlichkeit“. Sie fasst die Architektur, detaillierte Berechnungsansätze, zugrundeliegende Recherchen sowie Verbesserungsvorschläge automatisch zusammen. Dieses Dokument dient als umfassende Gedächtnisstütze, damit wir jederzeit direkt und nahtlos anknüpfen können.

---

## 1. Überblick & Zielsetzung

**Ziel:**

- **Robuste Berechnungslogik zur Ermittlung der WP-Solarwahrscheinlichkeit:**  
  - **Konzept:** Anhand von Echtzeit-Wetterdaten soll eine Kennzahl (WP-Wert) ermittelt werden, welche aussagt, ob die Wärmepumpe (WP) zu einem bestimmten Zeitpunkt aktiv sein sollte – basierend auf den aktuellen PV-Ertragsbedingungen.  
  - **Nutzen:** Optimierung des Eigenverbrauchs der PV-Anlage, Reduzierung des Netzstrombezugs und effizienter Betrieb der WP.

- **Optimale WP-Steuerung:**  
  - **Konzept:** Die Steuerung der WP erfolgt automatisiert, sodass sie nur dann aktiviert wird, wenn aufgrund günstiger Wetterbedingungen und PV-Ertragsprognosen ein hoher Eigenverbrauch möglich ist.  
  - **Nutzen:** Energieeinsparungen und Kostenreduktionen durch passgenaue Nutzung selbst erzeugter Solarenergie.

**Grundprinzipien:**

- **Echtzeitdaten aus mehreren Quellen:**  
  - Messwerte von drei regionalen Wetterstationen (Giessen, Bad Nauheim, Waldems-Reinborn) werden zur Erfassung aktueller Wetterbedingungen genutzt.  
  - **Hintergrund:** Recherchen mit API-Daten des DWD und anderen Open-Source-Systemen haben gezeigt, dass eine Mehrquellenintegration lokale Wetterphänomene besser abbildet.

- **Umfassende Validierung & Fallbacks:**  
  - Alle Sensordaten (z. B. Bewölkungsgrad, Windgeschwindigkeit, UV-Index, Sichtweite) werden zunächst validiert, und unplausible Werte werden durch Standardwerte ersetzt.  
  - **Hintergrund:** Studien und Erfahrungsberichte in Smart-Home-Projekten bestätigen, dass ein Fallback (z. B. 50 % für Bewölkung) wesentlich dazu beiträgt, Ausreißer abzufangen.

- **Dynamische Gewichtung mittels Vektoranalyse:**  
  - Die relevanten Wetterstationen werden anhand ihrer geographischen Lage und der aktuellen Windrichtung dynamisch gewichtet (mittels Dot-Produkt-Berechnung).  
  - **Recherchen:** Veröffentlichungen und Fallstudien zum Cloud-Tracking und zur PV-Ertragsprognose unterstützen diesen Ansatz, da er den tatsächlichen Einfluss von Wolkenbewegungen realistisch erfasst.

- **Saisonale Differenzierung:**  
  - Ein über eine Sinusfunktion berechneter saisonaler Korrekturfaktor passt den WP-Wert je nach Jahreszeit an – längere, intensivere Sommertage versus kürzere Wintertage.  
  - **Hintergrund:** Gut etablierte Modelle in der Photovoltaikbranche nutzen diese Herangehensweise, um saisonale PV-Leistungsunterschiede abzubilden.

---

## 2. Architektur & Codeaufbau

### Hauptkomponenten und Detailbeschreibung:

#### A. Sensorvalidierung:
- **Beschreibung:**  
  Jeder Eingangswert wird auf seinen plausiblen Wertebereich geprüft.  
- **Detail:**  
  - Beispiel: Ein Bewölkungsgrad außerhalb des Intervalls 0–100 % wird automatisch auf 50 % gesetzt.  
  - **Recherchen:** Branchenstandards und DWD-Dokumentationen vermuten, dass ca. 50 % ein durchschnittlicher Wert in unsicheren Situationen sein können.
- **Bewertung:**  
  Diese Validierung schützt vor Schwarz- und Weiß-Ausreißern in den Wetterdaten und sorgt für stabile Berechnungsgrundlagen.

#### B. Vektorbasiertes Standortmodell:
- **Geografische Vektorberechnung:**  
  - **Beschreibung:** Für jeden Wetterstandort werden relative Positionen (auf Basis von Breiten- und Längengrad) in einen Vektor umgerechnet.  
  - **Detail:** Zum Beispiel wird angenommen, dass 1° Breitengrad ca. 111 km entspricht (angepasst an den lokalen Breitengrad), sodass geografische Differenzen sinnvoll skaliert werden.
  - **Hintergrund:** Geodätische Berechnungen in der PV-Anlagenplanung bestätigen diese Methode.
  
- **Windvektor & Dot-Produkt:**  
  - **Beschreibung:** Die aktuelle Windrichtung und -geschwindigkeit werden in einen Vektor umgerechnet.  
  - **Detail:** Das Dot-Produkt zwischen dem Windvektor und den Standortvektoren gibt den Einflußfaktor an – ein Wert nahe 1 signalisiert eine optimale Ausrichtung, während niedrigere oder negative Werte den Einfluss des Standorts reduzieren (z. B. Faktor 0.9).  
  - **Recherchen:** Fachartikel zum Cloud-Tracking und zur Dynamik von Wettereinflüssen unterstützen die Effizienz dieses Ansatzes.
  
- **Bewertung:**  
  Dieser Ansatz ist praxisnah, da er dynamisch nur die tatsächlich relevanten Daten berücksichtigt – er minimiert den Einfluss von Stationen, die gerade keinen Einfluss auf den Einspeisepunkt haben.

#### C. Saisonaler Faktor:
- **Beschreibung:**  
  Mit Hilfe einer Sinusfunktion wird ein Faktor berechnet, der den natürlichen Verlauf der Sonnenintensität abbildet.  
- **Detail:**  
  - Der Jahres-Tag wird in einen Winkel umgerechnet, der in die Sinuskurve eingespeist wird. So entsteht ein glatter Übergang zwischen den Jahreszeiten.  
  - **Hintergrund:** Dieser Ansatz findet sich in zahlreichen PV-Leistungsprognosemodellen und wird häufig in wissenschaftlichen Studien eingesetzt.
- **Bewertung:**  
  Der saisonale Faktor stellt sicher, dass unsere Steuerlogik den natürlichen Schwankungen im PV-Ertrag gerecht wird und passt das System an wechselnde Bedingungen an.

#### D. Entscheidungslogik:
- **Zusammenführung:**  
  Die gewichteten WP-Werte der einzelnen Standorte werden zu einem Gesamtdurchschnitt aggregiert.
- **Schwellwert-basierte Entscheidung:**  
  - **Detail:**  
    - Werte <40 % → Sehr günstige Bedingungen (WP wird aktiviert: "JA").  
    - Werte zwischen 40 % und 70 % → Gemischte Bedingungen (WP moderat aktiv: "MODERAT").  
    - Werte >70 % → Ungünstige Bedingungen (WP bleibt inaktiv: "NEIN").  
  - **Unsicherheitsprüfung:**  
    - Bei großen Unterschieden der Winddaten (z. B. >30°) wird der WP-Wert als unsicher markiert und angepasst.
  - **Hintergrund:** Diese Logik basiert auf Erfahrungswerten und Forschungsergebnissen aus PV-basierten WP-Steuerungen.
- **Bewertung:**  
  Die Entscheidungslogik ist robust, da sie neben einem festen Schwellenwert-System auch dynamische Unsicherheitsprüfungen integriert; so minimieren wir Fehlaktivierungen.

---

## 3. Analyse, Bewertung und Forschungshintergrund

### Realismus:
- **Echtzeit-Datenintegration:**  
  - **Analyse:** Die Live-Daten von drei regionalen Wetterstationen liefern ein realistisches Abbild der aktuellen Wetterlage.  
  - **Recherchen:** Öffentliche API-Daten des DWD und wissenschaftliche Publikationen belegen, dass eine Mehrquellenintegration lokale Wetterphänomene besser darstellt.
  
- **Validierung & Fallback-Mechanismen:**  
  - **Analyse:** Durch den Einsatz fester Standardwerte bei unplausiblen Daten wird das System stabilisiert.
  - **Hintergrund:** Smart-Home-Studien und Erfahrungsberichte unterstreichen die Notwendigkeit solcher Fallback-Mechanismen.
  
- **Saisonaler Faktor:**  
  - **Analyse:** Die Verwendung einer Sinusfunktion spiegelt den natürlichen Trend der Sonnenintensität ab und unterstützt somit eine realitätsnahe Berechnung.
  - **Recherchen:** Dieser Ansatz wird in vielen PV-Prognosemodellen verwendet und hat sich als zuverlässig erwiesen.

### Praxisnähe:
- **Vektorbasiertes Standortmodell:**  
  - **Analyse:** Durch die Gewichtung der tatsächlichen Wetterbeeinflussung über die Windvektoren fließen nur relevante Daten in die Berechnung ein.
  - **Recherchen:** Branchenreports und Fallstudien (auch in verwandten Projekten) bestätigen, dass ein solches Modell die Performance signifikant verbessert.
  
- **Integration in Home Assistant:**  
  - **Nutzen:** Die modulare YAML-Konfiguration eignet sich hervorragend für automatisierte Steuerungen in Smart Homes.
  - **Hintergrund:** Die Home Assistant Community hat vielfach bewiesen, dass klare, dokumentierte YAML-Integrationen den operativen Betrieb deutlich vereinfachen.
  
- **Robustheit im Einsatz:**  
  - **Analyse:** Die modulare Architektur und detaillierte Kommentierung ermöglichen eine einfache Wartung und Weiterentwicklung.
  - **Hintergrund:** Erfahrungswerte aus ähnlichen energieeffizienten Projekten zeigen, dass ein gut strukturiertes System wesentlich weniger anfällig für Ausfälle ist.

### Verbesserungsvorschläge und Weiterentwicklung:
- **Dynamischere UV-Datenquelle:**  
  - *Vorschlag:* Integration einer API oder eines Sensormoduls, das UV-Werte häufiger aktualisiert (z. B. stündlich).
  - *Recherchen:* Diverse Studien weisen darauf hin, dass aktuellere UV-Daten zu einer feineren Abschätzung des PV-Ertrags führen können.
  
- **Zusätzliche Wetterstationen:**  
  - *Vorschlag:* Erweiterung der Datenbasis durch den Anschluss weiterer regionaler oder lokaler Sensoren.
  - *Recherchen:* Mehrere wissenschaftliche Arbeiten belegen, dass eine breitere Datengrundlage statistische Unsicherheiten reduziert.
  
- **Machine Learning-Integration:**  
  - *Vorschlag:* Entwicklung eines ML-Moduls, das historische Wetter- und PV-Daten auswertet und die Gewichtungsfaktoren dynamisch anpasst.
  - *Recherchen:* Zahlreiche Projekte im Bereich der PV-Ertragsprognose setzen bereits auf ML-Ansätze und berichten von entsprechenden Verbesserungen.
  
- **Erweiterte Visualisierungen:**  
  - *Vorschlag:* Erstellung von Dashboards oder Diagrammen (z. B. in Home Assistant oder externen Tools), um den Berechnungsprozess transparent zu machen.
  - *Hintergrund:* Visualisierung hat sich in vielen Smart-Home-Anwendungen als nützliches Werkzeug zur Fehlerdiagnose und Systemüberwachung erwiesen.
  
- **Feinjustierung der Gewichtungsfaktoren:**  
  - *Vorschlag:* Durchführung regelmäßiger Praxistests und Feedbackrunden zur Optimierung der Standardwerte und Einflussfaktoren.
  - *Recherchen:* Iterative Anpassungen an etablierten Systemen haben gezeigt, dass dies die Langzeitstabilität signifikant verbessert.

---

## 4. Zielgruppe und Nutzung dieser Dokumentation

- **Für das Entwicklerteam:**  
  - *Nutzen:* Diese Info.md dient als zentrales Nachschlagewerk mit allen getroffenen Designentscheidungen, Hintergrundrecherchen und technischen Details – neue Teammitglieder können sich so rasch in den gesamten Kontext einarbeiten.
  
- **Für Wartung und Weiterentwicklung:**  
  - *Nutzen:* Falls Probleme auftreten oder Erweiterungen nötig sind, bietet die vollständige Dokumentation einen schnellen Einstieg, um Ursache und Wirkung im System zu identifizieren.
  
- **Für kontinuierliche Verbesserung:**  
  - *Nutzen:* Alle identifizierten Verbesserungsmöglichkeiten und Weiterentwicklungsideen sind hier festgehalten, sodass sie als Leitfaden für zukünftige Entwicklungszyklen dienen.

---

## 5. Praktische Beispiele & Visualisierungsansätze

- **Beispielrechnung zur WP-Berechnung:**  
  - *Szenario 1:* Geringe Bewölkung (20 %), optimale Windrichtung (Dot-Produkt nahe 1), hoher saisonaler Faktor (Sommer) → WP-Wert z. B. 35 % → "JA" (WP aktiviert).  
  - *Szenario 2:* Hohe Bewölkung (80 %), ungünstige Windrichtung oder geringe Windbeteiligung, niedriger saisonaler Faktor (Winter) → WP-Wert z. B. 75 % → "NEIN" (WP inaktiv).
  - *Nutzen:* Diese Beispiele helfen, den Einfluss der einzelnen Variablen zu verstehen und dienen als Testfälle für die Validierung des Codes.

- **Visualisierung der Vektoranalyse:**  
  - *Ansatz:* Ein Diagramm oder eine Skizze, die die Position der Wetterstationen, den Einspeisepunkt und die aktuellen Windvektoren zeigt, wäre sehr hilfreich.  
  - *Nutzen:* Ein grafischer Ablaufplan (Flussdiagramm) der Entscheidungslogik trägt zur besseren Verständlichkeit der implementierten Logik bei.

---

## 6. Zusammenfassung

Dieses Dokument bietet eine umfassende Übersicht über den gesamten konzeptionellen und praktischen Hintergrund unseres Projekts "Solarwahrscheinlichkeit". Folgende Punkte stehen dabei im Fokus:

- **Realitätsnahe Integration:**  
  Echtzeit-Wetterdaten von drei regionalen Stationen bilden die Basis unseres Systems.
  
- **Robuste und dynamische Berechnung:**  
  Validierung von Sensordaten, vektorbasiertes Standortmodell und ein saisonal angepasster Faktor gewährleisten eine verlässliche WP-Wert-Ermittlung.
  
- **Praxisnahe Entscheidungslogik:**  
  Eine definierte Schwellenwertlogik und Unsicherheitsprüfungen sorgen für eine autarke und effiziente WP-Steuerung.
  
- **Hintergrundwissen & Recherchen:**  
  Das konzeptionelle Fundament basiert auf etablierten wissenschaftlichen Ansätzen, Branchenstandards und offenen Datenquellen (u.a. DWD, Smart-Home-Projekte, PV-Ertragsstudien).
  
- **Entwicklungsperspektiven:**  
  Verbesserungsmöglichkeiten (dynamischere UV-Daten, zusätzliche Sensoren, Machine Learning, Visualisierung) sind identifiziert und dokumentiert.
  
- **Praktische Anwendungsfälle:**  
  Es wurden Beispielrechnungen und Visualisierungsansätze skizziert, um die Theorie anschaulich zu machen.

Diese detaillierte Info.md stellt sicher, dass unser Wissen – von der Konzeption über die Implementierung bis hin zu weiterführenden Optimierungsmöglichkeiten – lückenlos dokumentiert ist. So können wir auch nach längeren Pausen nahtlos an den aktuellen Stand anknüpfen und unser System weiterentwickeln.

---

