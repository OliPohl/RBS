const maxTime = 240; // Anzeige auf die nächsten 4 Stunden begrenzt => Begrenzung der maximalen Buchungslänge auf 4 Stunden?
const standardValueTime = '0'; // wird als Startwert für das Attribut remainingTime verwendet => sollte sich die Konstante im Javascript ändern, muss auch das CSS angepasst werden
const dataURL = "js/data.json"; // JSON-Datei mit den Daten
var rooms = new Array;


/* Jeder Eintrag (Entry) ist eine Buchung */
class Entry {
  constructor() {
    this.userId = new String(); // Hochschulausweis-ID
    this.entryTime = new Date(); // Zeitpunkt der Buchung
    this.exitTime = new Date(); // Zeitpunkt, zudem die Buchung automatisch aufhören soll; wird aus der Länge der Buchung errechnet (das ist aber noch nicht implementiert)
  }

  remainingTime() { // gibt an, wie lange eine Buchung noch dauert (in Minuten)
    // aktuell wird die Dauer zwischen Startzeitpunkt und Endzeitpunkt ausgegeben; für die spätere Anwendung sollte die Dauer zwischen aktuellem Zeitpunkt und Endzeitpunkt ausgegeben werden
    return Math.round((Date.parse(this.exitTime) - Date.parse(this.entryTime)) / 60000);
  }
}

class Room {
  constructor(id,isActive,loudSeats,quietSeats,size,x,y) {
    this.id = id;
    this.isActive = isActive;
    this.loudSeats = loudSeats;
    this.quietSeats = quietSeats;
    this.size = size;
    this.x = x; // X-Koordinate auf der Karte; angegeben in CSS-Einheiten
    this.y = y; // Y-Koordinate auf der Karte; angegeben in CSS-Einheiten

    this.roomState = "Empty"; // Status des Raums (empty, full, quiet, loud)
    this.entry = new Array(size);
    for (let i = 0; i < size; i++) {
      this.entry[i] = new Entry;
    }
  }

  occupation() { // gibt an, wie voll ein Raum ist
    let result = 0;
    for (let i = 0; i < this.size; i++) {
      if (this.entry[i].userId != "") {
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
    rooms.push(new Room(
      roomsJSON.rooms[i]._id,
      roomsJSON.rooms[i].isActive,
      roomsJSON.rooms[i].loudSeats,
      roomsJSON.rooms[i].quietSeats,
      roomsJSON.rooms[i].entry.length,
      roomsJSON.rooms[i].x,
      roomsJSON.rooms[i].y
    ));
  }
}

async function updateData() { //wenn neue Räume hinzugefügt werden, muss die Seite aktualisiert werden
  let request = new Request(dataURL);
  let response = await fetch(request);
  let roomsJSON = await response.json();

  for (let i = 0; i < roomsJSON.rooms.length; i++) {
    rooms[i].roomState = roomsJSON.rooms[i].roomState;
    rooms[i].size = roomsJSON.rooms[i].entry.length;
    rooms[i].entry = new Array(rooms[i].size);
    for (let j = 0; j < rooms[i].size; j++) {
      rooms[i].entry[j] = new Entry;
      rooms[i].entry[j].userId = roomsJSON.rooms[i].entry[j].userId;
      if (rooms[i].entry[j].userId != "") {
        rooms[i].entry[j].entryTime = roomsJSON.rooms[i].entry[j].entryTime;
        rooms[i].entry[j].exitTime = roomsJSON.rooms[i].entry[j].exitTime;
      } else {
        rooms[i].entry[j].entryTime = new Date();
        rooms[i].entry[j].exitTime = new Date();
      }
    }
    if (((rooms[i].roomState == "Quiet") && (rooms[i].occupation() == rooms[i].quietSeats)) || ((rooms[i].roomState == "Loud") && (rooms[i].occupation() == rooms[i].loudSeats))) {
      rooms[i].roomState = "full";
    }
    if ((rooms[i].occupation() == 0) && (rooms[i].roomState != "Empty")) { // nur zur Sicherheit; eigentlich (wenn alles funktioniert bei der Tür, der Datenbank und der Verbindung) sollte dieser Fall nicht eintreten
      rooms[i].roomState = "Empty";
    } else if ((rooms[i].occupation() != 0) && (rooms[i].roomState == "Empty")) {
      rooms[i].size = 0;
      rooms[i].entry = new Array(0);
    }
  }
}

async function buildHTML() {
  await getData();
  let wrapper = document.querySelector(".wrapper");
  let htmlElement = new String();
  for (let i = 0; i < rooms.length; i++) {
    if (rooms[i].isActive == "True") {
      htmlElement = '<div class="room ' + rooms[i].roomState + '" id="' + rooms[i].id + '" style="left: ' + rooms[i].x + '; top: ' + rooms[i].y + '"><h3>' + rooms[i].id + '</h3>';
      for (let j = 0; j < Math.max(rooms[i].loudSeats,rooms[i].quietSeats); j++) {
        htmlElement += '<div class="bar" remainingTime="' + standardValueTime + '" style="width: 0"></div>';
      }
      htmlElement += '</div>';
      wrapper.innerHTML += htmlElement;
    }
  }
}

function updateRoom(room = new Room()) {
  let htmlroom = document.getElementById(room.id);
  htmlroom.classList.replace(htmlroom.classList[1], room.roomState); //Raumstatus wird geupdatet
  switch (room.roomState) { //Anzahl der belegten Plätze auf der Anzeige wird geupdatet
    case "Loud": {
      htmlroom.querySelector("h3").innerHTML = room.id + ' (' + room.occupation() + ' von ' + room.loudSeats + ' Plätzen belegt)';
      break;
    }
    case "Quiet": {
      htmlroom.querySelector("h3").innerHTML = room.id + ' (' + room.occupation() + ' von ' + room.quietSeats + ' Plätzen belegt)';
      break;
    }
    case "Full": {
      htmlroom.querySelector("h3").innerHTML = room.id + ' (' + room.occupation() + ' von ' + room.occupation() + ' Plätzen belegt)';
      break;
    }
    default: {
      htmlroom.querySelector("h3").innerHTML = room.id;
      break;
    }
  }
  let bars = htmlroom.querySelectorAll(".bar"); //die einzelnen Balken der Einträge werden geupdatet
  //Zeiten sollen im Objekt nach Länge geordnet werden
  let timeDif = new Number();
  for (let i = 0; i < room.entry.length; i++) {
    timeDif = room.entry[i].remainingTime();
    if (timeDif >= 0) { //einfach nur um Fehler vorzubeugen (z.B. Rundungsfehler)
      bars[i].setAttribute('remainingTime', timeDif); //Zeit wird geupdatet
      bars[i].setAttribute('style', 'width: calc((' + timeDif + ' / ' + maxTime + ') * (100% - 2rem))'); //Balkenlänge wird geupdatet
    } else {
      bars[i].setAttribute('remainingTime', standardValueTime); //Zeit wird geupdatet
      bars[i].setAttribute('style', 'width: 0'); //Balkenlänge wird geupdatet
    }
  }
  for (let i = room.entry.length; i < bars.length; i++) {
    bars[i].setAttribute('remainingTime', standardValueTime); //Zeit wird geupdatet
    bars[i].setAttribute('style', 'width: 0'); //Balkenlänge wird geupdatet
  }
}

function updateBarsLength(room = new Room()) { // bisher ungenutzt; aber gute Möglichkeit um benötigte Rechenpower runterzukriegen, wenn es einen Changelog gibt
  let htmlroom = document.getElementById(room.id);
  let bars = htmlroom.querySelectorAll(".bar"); //die einzelnen Balken der Einträge werden geupdatet
  //Zeiten sollen im Objekt nach Länge geordnet werden
  let timeDif = new Number();
  for (let i = 0; i < room.entry.length; i++) {
    timeDif = room.entry[i].remainingTime();
    if (timeDif >= 0) { //einfach nur um Fehler vorzubeugen (z.B. Rundungsfehler)
      bars[i].setAttribute('remainingTime', timeDif); //Zeit wird geupdatet
      bars[i].setAttribute('style', 'width: calc((' + timeDif + ' / ' + maxTime + ') * (100% - 2rem))'); //Balkenlänge wird geupdatet
    } else {
      bars[i].setAttribute('remainingTime', standardValueTime); //Zeit wird geupdatet
      bars[i].setAttribute('style', 'width: 0'); //Balkenlänge wird geupdatet
    }
  }
  for (let i = room.entry.length; i < bars.length; i++) {
    bars[i].setAttribute('remainingTime', standardValueTime); //Zeit wird geupdatet
    bars[i].setAttribute('style', 'width: 0'); //Balkenlänge wird geupdatet
  }
}

async function updateHTML() {
  await updateData();
  for (let i = 0; i < rooms.length; i++) {
    if (rooms[i].isActive == "True") {
      updateRoom(rooms[i]);
    }
  }
}




buildHTML();
setTimeout(() =>
{
  setInterval(updateHTML, 2000);
}, 1000);
