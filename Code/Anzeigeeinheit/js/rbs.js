const maxTime = 240; // Anzeige auf die nächsten 4 Stunden begrenzt => Begrenzung der maximalen Buchungslänge auf 4 Stunden?
const standardValueTime = '0 min'; // wird als Startwert für das Attribut remainingTime verwendet => sollte sich die Konstante im Javascript ändern, muss auch das CSS angepasst werden
const dataURL = "js/data.json"; // JSON-Datei mit den Daten
var rooms = new Array;


/* Jeder Eintrag (Entry) ist eine Buchung */
class Entry {
  constructor() {
    this.id = new String(); // Hochschulausweis-ID
    this.startTime = new Date(); // Zeitpunkt der Buchung
    this.endTime = new Date(); // Zeitpunkt, zudem die Buchung automatisch aufhören soll; wird aus der Länge der Buchung errechnet (das ist aber noch nicht implementiert)
  }

  remainingTime() { // gibt an, wie lange eine Buchung noch dauert (in Minuten)
    // aktuell wird die Dauer zwischen Startzeitpunkt und Endzeitpunkt ausgegeben; für die spätere Anwendung sollte die Dauer zwischen aktuellem Zeitpunkt und Endzeitpunkt ausgegeben werden
    return Math.round((Date.parse(this.endTime) - Date.parse(this.startTime)) / 60000);
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

  occupation() { // gibt an, wie voll ein Raum ist
    let result = 0;
    for (let i = 0; i < this.size; i++) {
      if (this.entries[i].id != "") {
        result++;
      }
    }
    return result;
  }
}


/* Testdaten */
//var rooms = [new Room("A226",2,"0","0"),new Room("C125",3,"50%","25%"),new Room("F125",2,"25%","60%")];


/* Daten aus JSON-Datei ziehen */
async function getData() {
  let request = new Request(dataURL);
  let response = await fetch(request);
  let roomsJSON = await response.json();

  for (let i = 0; i < roomsJSON.rooms.length; i++) {
    rooms.push(new Room(roomsJSON.rooms[i].id,roomsJSON.rooms[i].size,roomsJSON.rooms[i].x,roomsJSON.rooms[i].y));
  }
}

async function updateData() {
  let request = new Request(dataURL);
  let response = await fetch(request);
  let roomsJSON = await response.json();

  for (let i = 0; i < roomsJSON.rooms.length; i++) {
    rooms[i].state = roomsJSON.rooms[i].state;
    for (let j = 0; j < rooms[i].size; j++) {
      rooms[i].entries[j].id = roomsJSON.rooms[i].entries[j].id;
      if (rooms[i].entries[j].id != "") {
        rooms[i].entries[j].startTime = roomsJSON.rooms[i].entries[j].startTime;
        rooms[i].entries[j].endTime = roomsJSON.rooms[i].entries[j].endTime;
      } else {
        rooms[i].entries[j].startTime = new Date();
        rooms[i].entries[j].endTime = new Date();
      }
    }
  }
}

async function buildHTML() {
  await getData();
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

function updateRoom(room = new Room()) {
  let htmlroom = document.getElementById(room.id);
  htmlroom.classList.replace(htmlroom.classList[1], room.state); //Raumstatus wird geupdatet
  htmlroom.querySelector("h3").innerHTML = room.id + ' (' + room.occupation() + ' von ' + room.size + ' Plätzen belegt)'; //Anzahl der belegten Plätze auf der Anzeige wird geupdatet
  let bars = htmlroom.querySelectorAll(".bar"); //die einzelnen Balken der Einträge werden geupdatet
  //Zeiten sollen im Objekt nach Länge geordnet werden
  let timeDif = new Number();
  for (let i = 0; i < bars.length; i++) {
    timeDif = room.entries[i].remainingTime();
    bars[i].setAttribute('remainingTime', timeDif + ' min'); //Zeit wird geupdatet
    bars[i].setAttribute('style', 'width: calc((' + timeDif + ' / ' + maxTime + ') * 100%)'); //Balkenlänge wird geupdatet
  }
}

function updateBarsLength(room = new Room()) { // bisher ungenutzt; aber gute Möglichkeit um benötigte Rechenpower runterzukriegen, wenn es einen Changelog gibt
  let testTime = 3; //hier muss noch eine ordentliche Formel hin
  let htmlroom = document.getElementById(room.id);
  let bars = htmlroom.querySelectorAll(".bar"); //die einzelnen Balken der Einträge werden geupdatet
  //Zeiten sollen im Objekt nach Länge geordnet werden
  for (let i = 0; i < bars.length; i++) {
    bars[i].setAttribute('remainingTime', testTime + ' min'); //Zeit wird geupdatet
    bars[i].setAttribute('style', 'width: calc((' + testTime + ' / ' + maxTime + ') * 100%)'); //Balkenlänge wird geupdatet
  }
}

async function updateHTML() {
  await updateData();
  for (let i = 0; i < rooms.length; i++) {
    updateRoom(rooms[i]);
  }
}




buildHTML();
setTimeout(() =>
{
  setInterval(updateHTML, 2000);
}, 1000);
