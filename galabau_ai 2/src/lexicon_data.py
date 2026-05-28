"""Öffentliche Lern- und Nachschlagedaten für den GaLaBau Coach."""

LEXICON_SOURCES = [
    {
        "label": "BIBB – Berufsprofil Gärtner/in, Fachrichtung Garten- und Landschaftsbau",
        "url": "https://www.bibb.de/dienst/berufesuche/de/index_berufesuche.php/profile/apprenticeship/98765432",
        "note": "Öffentliche Übersicht zu beruflicher Handlungsfähigkeit und Tätigkeitsfeldern.",
    },
    {
        "label": "Gärtnerausbildungsverordnung – GärtnAusbV, insb. § 11 und Anlagen",
        "url": "https://www.gesetze-im-internet.de/g_rtnausbv/",
        "note": "Rechtsgrundlage der Berufsausbildung und Abschlussprüfung.",
    },
    {
        "label": "KMK – Rahmenlehrplan Gärtner/Gärtnerin",
        "url": "https://www.kmk.org/fileadmin/Dateien/pdf/Bildung/BeruflicheBildung/rlp/Gaertner95-12-08.pdf",
        "note": "Lernfelder der Berufsschule.",
    },
    {
        "label": "Landwirtschaftskammer NRW – Lehrgangsinhalte Garten- und Landschaftsbau",
        "url": "https://www.landwirtschaftskammer.de/gartenbau/ausbildung/lehrgaenge/galabau.htm",
        "note": "Überbetriebliche Lehrgangsinhalte, z. B. Pflaster, Naturstein, Pflanzenverwendung.",
    },
    {
        "label": "Landschaftsgärtner.com – Ausbildungsinhalte",
        "url": "https://www.landschaftsgaertner.com/ausbildungsinhalte",
        "note": "Branchenportal mit Ausbildungsüberblick.",
    },
    {
        "label": "Bundesagentur für Arbeit BERUFENET – Gärtner/in GaLaBau",
        "url": "https://web.arbeitsagentur.de/berufenet/beruf/588",
        "note": "Berufsbild und Ausbildungsdauer.",
    },
]

LEXICON = [
    {"bereich": "Ausbildung & Prüfung", "titel": "Berufsbild Landschaftsgärtner/in", "kurz": "Duale dreijährige Ausbildung im Garten- und Landschaftsbau.", "inhalt": "Typische Lern- und Arbeitsfelder sind Baustellen einrichten und abwickeln, Erdarbeiten, Be- und Entwässerung, befestigte Flächen, Außenanlagen, Pflanzenverwendung und Pflege.", "tags": ["Ausbildung", "Berufsbild", "Prüfung"], "quelle": "BIBB Berufsprofil; BERUFENET"},
    {"bereich": "Ausbildung & Prüfung", "titel": "Abschlussprüfung GaLaBau", "kurz": "Praktische, schriftliche und mündliche Prüfung.", "inhalt": "Die Abschlussprüfung der Fachrichtung Garten- und Landschaftsbau bezieht sich auf die im Ausbildungsrahmenplan aufgeführten Fertigkeiten und Kenntnisse sowie den wesentlichen Berufsschulstoff.", "tags": ["GärtnAusbV", "Prüfung"], "quelle": "GärtnAusbV § 11"},
    {"bereich": "Pflanzenkunde", "titel": "Lavandula angustifolia – Echter Lavendel", "kurz": "Halbstrauch für sonnige, trockene Standorte.", "inhalt": "Merkmale: schmale graugrüne Blätter, violette Blüten, aromatischer Duft. Verwendung: Staudenbeete, mediterrane Pflanzungen, Bienenweide. Pflege: durchlässiger Boden, Staunässe vermeiden, Rückschnitt nach der Blüte bzw. im Frühjahr.", "tags": ["Pflanze", "Staude", "Trockenstandort"], "quelle": "Allgemeine Pflanzenkunde; mit Unterrichtsmaterial abgleichen"},
    {"bereich": "Pflanzenkunde", "titel": "Buxus sempervirens – Gewöhnlicher Buchsbaum", "kurz": "Immergrünes Form- und Einfassungsgehölz.", "inhalt": "Merkmale: kleine immergrüne Blätter, gut schnittverträglich. Verwendung: Einfassungen, Formschnitt, historische Gärten. Achtung: Buchsbaumzünsler und Pilzkrankheiten beachten; Alternativen können standortabhängig sinnvoll sein.", "tags": ["Gehölz", "Formschnitt", "Pflege"], "quelle": "Allgemeine Pflanzenkunde; Pflanzenschutz aktuell prüfen"},
    {"bereich": "Pflanzenkunde", "titel": "Hydrangea macrophylla – Gartenhortensie", "kurz": "Blühstrauch für frische bis feuchte, humose Standorte.", "inhalt": "Merkmale: große Blütenbälle oder Tellerblüten, gegenständige Blätter. Verwendung: halbschattige Beete, Vorgärten, Kübel. Pflege: gleichmäßige Wasserversorgung; Schnitt abhängig von Sorte und Blühverhalten.", "tags": ["Gehölz", "Blüte", "Halbschatten"], "quelle": "Allgemeine Pflanzenkunde; Sortenangaben prüfen"},
    {"bereich": "Pflanzenkunde", "titel": "Taxus baccata – Europäische Eibe", "kurz": "Immergrünes, sehr schnittverträgliches Nadelgehölz.", "inhalt": "Verwendung: Hecken, Formschnitt, Sichtschutz. Standort: schattentolerant, humoser bis normaler Gartenboden. Sicherheit: Pflanzenteile sind giftig; Umgang und Beratung entsprechend vorsichtig.", "tags": ["Gehölz", "Hecke", "Giftpflanze"], "quelle": "Allgemeine Pflanzenkunde; Giftpflanzenhinweise prüfen"},
    {"bereich": "Bodenkunde", "titel": "Bodenarten: Sand, Schluff, Ton", "kurz": "Die Korngrößen bestimmen Wasser- und Nährstoffhaushalt.", "inhalt": "Sandige Böden sind gut durchlüftet und wasserdurchlässig, speichern aber weniger Wasser und Nährstoffe. Tonige Böden speichern viel Wasser und Nährstoffe, können aber verdichten. Schluffige Böden liegen dazwischen und sind erosionsanfällig.", "tags": ["Boden", "Standort", "Pflanzenverwendung"], "quelle": "Berufsschul-Grundlagen Bodenkunde"},
    {"bereich": "Pflasterbau", "titel": "Schichten im Pflasteraufbau", "kurz": "Planum, Frostschutz/Tragschicht, Bettung, Pflasterdecke, Fugen.", "inhalt": "Ein tragfähiger Pflasteraufbau beginnt mit einem ausreichend verdichteten Planum. Darauf folgen Frostschutz- bzw. Tragschichten, eine gleichmäßige Bettung und die Pflasterdecke mit passenden Fugen. Gefälle und Randeinfassung sind für Entwässerung und Stabilität wesentlich.", "tags": ["Pflaster", "Wegebau", "Bautechnik"], "quelle": "LWK NRW Lehrgangsinhalte; Unterrichtsmaterial/FLL-ZTV prüfen"},
    {"bereich": "Pflasterbau", "titel": "Gefälle im Außenbereich", "kurz": "Wasser muss sicher von Gebäuden und Nutzflächen abgeleitet werden.", "inhalt": "Bei befestigten Flächen ist ein funktionsfähiges Gefälle ein zentraler Ausführungs- und Kontrollpunkt. Die konkrete Ausführung hängt von Belag, Nutzung, Entwässerung und technischen Regelwerken ab.", "tags": ["Entwässerung", "Pflaster", "Baustelle"], "quelle": "Berufsschule/überbetriebliche Ausbildung; technische Regelwerke prüfen"},
    {"bereich": "Treppenbau", "titel": "Schrittmaßregel", "kurz": "Orientierungsformel für angenehm begehbare Treppen.", "inhalt": "Die bekannte Faustformel lautet: 2 x Steigung + Auftritt ≈ 63 cm. Sie dient als Lern- und Kontrollhilfe; konkrete Anforderungen sind anhand der einschlägigen Normen, Planung und Baustellensituation zu prüfen.", "tags": ["Treppe", "Rechnen", "Bautechnik"], "quelle": "Berufsschul-Grundlagen; DIN-Anforderungen aktuell prüfen"},
    {"bereich": "Naturstein & Mauerbau", "titel": "Trockenmauer", "kurz": "Mauer ohne Mörtel, Stabilität durch Verband, Neigung und Hinterfüllung.", "inhalt": "Wichtige Punkte sind ein tragfähiges Fundament, ausreichende Hinterfüllung/Dränage, versetzte Stoßfugen und geeignetes Steinmaterial. Trockenmauern können ökologisch wertvoll sein, z. B. als Lebensraum für Insekten und Reptilien.", "tags": ["Naturstein", "Mauer", "Ökologie"], "quelle": "LWK NRW Lehrgangsinhalte; Fachregeln prüfen"},
    {"bereich": "WIPO & Recht", "titel": "Ausbildungsvertrag", "kurz": "Regelt wesentliche Rechte und Pflichten der Ausbildung.", "inhalt": "Typische Inhalte sind Ausbildungsziel, Beginn und Dauer, Probezeit, Vergütung, Arbeitszeit, Urlaub und Pflichten von Ausbildendem und Auszubildendem. Für Details sind BBiG, Vertrag und Kammerinformationen maßgeblich.", "tags": ["WIPO", "Ausbildung", "Recht"], "quelle": "BBiG/Unterrichtsmaterial; Kammerunterlagen prüfen"},
    {"bereich": "WIPO & Recht", "titel": "Abnahme im Werkvertragsrecht", "kurz": "Wichtiger Zeitpunkt bei Bau- und Werkleistungen.", "inhalt": "Die Abnahme ist im Werkvertragsrecht ein zentraler rechtlicher Anknüpfungspunkt, u. a. für Fälligkeit, Gefahrübergang und Mängelrechte. Im GaLaBau sollte sie sauber dokumentiert werden.", "tags": ["Baurecht", "BGB", "Dokumentation"], "quelle": "BGB-Werkvertragsrecht; VOB/B nur bei wirksamer Vereinbarung prüfen"},
    {"bereich": "Arbeitsschutz", "titel": "Persönliche Schutzausrüstung", "kurz": "PSA richtet sich nach Tätigkeit und Gefährdungsbeurteilung.", "inhalt": "Typische PSA im GaLaBau umfasst Sicherheitsschuhe, Handschuhe, Augen-/Gehörschutz, Warnkleidung und je nach Tätigkeit Helm oder Schnittschutz. Maßgeblich sind Unterweisung, Betriebsanweisung und Gefährdungsbeurteilung.", "tags": ["Arbeitsschutz", "Baustelle", "PSA"], "quelle": "Arbeitsschutz-Unterweisung; DGUV/Betriebsanweisungen prüfen"},
]

QUICK_QUESTIONS = [
    "Was muss ich beim Pflasteraufbau prüfen?",
    "Erkläre die Schrittmaßregel mit Beispiel.",
    "Welche Pflanzen passen zu trockenen, sonnigen Standorten?",
    "Was gehört in eine Baustellendokumentation?",
    "Welche Rechte und Pflichten habe ich als Azubi?",
]
