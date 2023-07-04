const maxTime = 90; // Anzeige auf die nächsten 90 Minuten begrenzt => das ist die maximale Dauer einer Buchung in der Türeinheit
const standardValueTime = '0'; // wird als Startwert für das Attribut remainingTime verwendet => sollte sich die Konstante im Javascript ändern, muss auch das CSS angepasst werden
const dataURL = "js/data.json"; // JSON-Datei mit den Daten
var rooms = new Array;
const updateFrequency = 30000; // Aktualisierungsrate in Millisekunden


/* Jeder Eintrag (Entry) ist eine Buchung */
class Entry {
  constructor() {
    this.userId = new String(); // Hochschulausweis-ID
    this.entryTime = new Date(); // Zeitpunkt der Buchung => im Prinzip nur zum Testen relevant, danach für die zentrale Anzeige nicht mehr relevant
    this.exitTime = new Date(); // Zeitpunkt, zudem die Buchung automatisch aufhört
  }

  remainingTime() { // gibt an, wie lange eine Buchung noch dauert (in Minuten)
    // obere Zeile wird die Dauer zwischen Startzeitpunkt und Endzeitpunkt ausgegeben (für Testzwecke sinnvoll); für die spätere Anwendung sollte die Dauer zwischen aktuellem Zeitpunkt und Endzeitpunkt ausgegeben werden (untere Zeile)
    //return Math.round((Date.parse(this.exitTime) - Date.parse(this.entryTime)) / 60000);
    return Math.round((Date.parse(this.exitTime) - Date.now()) / 60000);
  }
}

class Room {
  constructor(id,isActive,loudSeats,quietSeats,x,y) {
    this.id = id;
    this.isActive = isActive;
    this.loudSeats = loudSeats;
    this.quietSeats = quietSeats;
    this.size = 0;
    this.x = x; // X-Koordinate auf der Karte; angegeben in CSS-Einheiten
    this.y = y; // Y-Koordinate auf der Karte; angegeben in CSS-Einheiten

    this.roomState = "Empty"; // Status des Raums (Empty, Full, Quiet, Loud)
    this.entry = new Array(0);
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
      parseInt(roomsJSON.rooms[i].loudSeats),
      parseInt(roomsJSON.rooms[i].quietSeats),
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
    rooms[i].entry = new Array(0);
    for (let j = 0; j < roomsJSON.rooms[i].entry.length; j++) {

      e = new Entry;
      e.userId = roomsJSON.rooms[i].entry[j].userId;
      if (e.userId != "") {
        e.entryTime = roomsJSON.rooms[i].entry[j].entryTime;
        e.exitTime = roomsJSON.rooms[i].entry[j].exitTime;
      } else {
        e.entryTime = new Date();
        e.exitTime = new Date();
      }
      if (e.remainingTime() > 0) {
        rooms[i].entry[rooms[i].entry.length] = e;
      }
    }
    rooms[i].size = rooms[i].entry.length;
    if (((rooms[i].roomState == "Quiet") && (rooms[i].occupation() == rooms[i].quietSeats)) || ((rooms[i].roomState == "Loud") && (rooms[i].occupation() == rooms[i].loudSeats)) || (rooms[i].roomState == "Blocked")) {
      rooms[i].roomState = "Full";
    }
    if ((rooms[i].occupation() == 0) && (rooms[i].roomState != "Empty")) { // nur zur Sicherheit; eigentlich (wenn alles funktioniert bei der Tür, der Datenbank und der Verbindung zwischen allem) sollte dieser Fall nicht eintreten
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
  //Zeiten sollen im Objekt nach Länge geordnet werden (kommt später, weil nur für schön aussehen)
  let timeDif = new Number();
  for (let i = 0; i < room.entry.length; i++) {
    timeDif = room.entry[i].remainingTime();
    if (timeDif >= 0) {
      bars[i].setAttribute('remainingTime', timeDif); //Zeit wird geupdatet
      if (timeDif <= maxTime) {
        bars[i].setAttribute('style', 'width: calc((' + timeDif + ' / ' + maxTime + ') * (100% - 2rem))'); //Balkenlänge wird geupdatet
      } else {
        bars[i].setAttribute('style', 'width: calc(100% - 2rem)');
      }
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
  updateHTML();
  setInterval(updateHTML, updateFrequency);
}, 1000);
