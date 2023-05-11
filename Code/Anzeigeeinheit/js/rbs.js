/* Jeder Eintrag (Entry) ist eine Buchung */
class Entry {
  constructor() {
    this.id = new String(); // Hochschulausweis-ID
    this.startTime = new Date(); // Zeitpunkt der Buchung
    this.endTime = new Date(); // Zeitpunkt, zudem die Buchung automatisch aufhören soll; wird aus der Länge der Buchung errechnet (das ist aber noch nicht implementiert)
  }
}

class Room {
  constructor(id,size,x,y) {
    this.id = id;
    this.size = size;
    this.x = x; // X-Koordinate auf der Karte; angegeben in CSS-Einheiten
    this.y = y; // Y-Koordinate auf der Karte; angegeben in CSS-Einheiten

    this.state = "empty"; // Status des Raums (empty, full, quiet, loud)
    this.entries = new Array(size);
    for (let i = 0; i < size; i++) {
      this.entries[i] = new Entry();
    }
  }
}


/* Daten aus JSON-Datei ziehen */
var rooms = [new Room("A226",2,"0","0"),new Room("C125",3,"50%","25%"),new Room("F125",2,"25%","60%")];

const maxTime = 240; // Anzeige auf die nächsten 4 Stunden begrenzt => Begrenzung der maximalen Buchungslänge auf 4 Stunden?
const standardValueTime = ''; // wird als Startwert für das Attribut remainingTime verwendet => sollte sich die Konstante im Javascript ändern, muss auch das CSS angepasst werden

/* baut erstmal alle Räume im HTML */
{
  let wrapper = document.querySelector(".wrapper");
  let htmlElement = new String();
  let j = new Number();
  for (let i = 0; i < rooms.length; i++) {
    htmlElement = '<div class="room ' + rooms[i].state + '" id="' + rooms[i].id + '" style="left: ' + rooms[i].x + '; top: ' + rooms[i].y + '"><h3>' + rooms[i].id + ' (0 von ' + rooms[i].size + ' Plätzen belegt)</h3>';
    for (j = 0; j < rooms[i].size; j++) {
      htmlElement += '<div class="bar" remainingTime="' + standardValueTime + '" style="width: calc((' + 0 + ' / ' + maxTime + ') * 100%)"></div>';
    }
    htmlElement += '</div>';
    wrapper.innerHTML += htmlElement;
  }
}
