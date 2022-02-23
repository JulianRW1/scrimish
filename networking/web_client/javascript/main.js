var websocket;

const IMAGE_SCALE = 50;

var activeGames = [];

const AVAILABLE_GAMES = 'available games';


window.addEventListener("DOMContentLoaded", () => {
    // Open WebSocket connection and register event handlers
    // websocket = new WebSocket("ws://192.168.1.17:8001/"); 
    websocket = new WebSocket("ws://localhost:8001/"); 

    recieveEvents(websocket);
    
    // Initialize the UI
    initHomepage();

    // board = createBoard();

});

function initHomepage() {
    // create home page panel
    let homepagePanel = document.createElement('div');
    homepagePanel.className = 'homepage';
    document.body.appendChild(homepagePanel);

    // create left panel
    let leftHomeScreen = document.createElement('div');
    leftHomeScreen.className = 'leftHomeScreen';
    homepagePanel.appendChild(leftHomeScreen);

    // panel for refresh button
    let gameOptions = document.createElement('div');
    gameOptions.className = 'gameOptions';
    leftHomeScreen.appendChild(gameOptions);
    
    // create games panel
    let gamesPanel = document.createElement('div');
    gamesPanel.className = 'gamesPanel';
    gamesPanel.id = 'gamesPanel';
    leftHomeScreen.appendChild(gamesPanel);

    //add games to gamesPanel
    let gamesTable = document.createElement('table');
    gamesTable.className = 'gamesTable';
    gamesTable.id = 'gamesTable';
    gamesPanel.appendChild(gamesTable);

    refreshBtn = makeButton(parent=gameOptions, text='⟳ Refresh', className= 'refreshGamesBtn', refreshGames);

    // Query the server for the available games when socket opens
    websocket.onopen = () => send(new Query(AVAILABLE_GAMES)); 

    // create right panel
    let rightHomeScreen = document.createElement('div');
    rightHomeScreen.className = 'rightHomeScreen';
    homepagePanel.appendChild(rightHomeScreen);

    let gameSettingsPanel = document.createElement('div');
    gameSettingsPanel.className = 'gameSettingsPanel';
    rightHomeScreen.appendChild(gameSettingsPanel);

    let levelSelectLbl = document.createElement('label');
    levelSelectLbl.innerHTML = 'Choose Your Level:';
    gameSettingsPanel.appendChild(levelSelectLbl);

    let levelSelect = createDropDownSelect(['Novice', 'Beginner','Intermediate','Advanced','Expert']);
    levelSelect.id = 'levelSelect';
    gameSettingsPanel.appendChild(levelSelect);

    let speedSelectLbl = document.createElement('label');
    speedSelectLbl.innerHTML = 'Choose Game Speed:';
    gameSettingsPanel.appendChild(speedSelectLbl);

    let speedSelect = createDropDownSelect(['Very Slow', 'Slow', 'Normal', 'Fast', 'Very Fast']);
    speedSelect.options[2].selected = 'selected'; // Select normal by default
    speedSelect.id = 'speedSelect';
    gameSettingsPanel.appendChild(speedSelect);

    let playerSelectLbl = document.createElement('label');
    playerSelectLbl.innerHTML = 'Player Count:';
    gameSettingsPanel.appendChild(playerSelectLbl);

    let playersSelect = createDropDownSelect([2, 3, 4]);
    playersSelect.id = 'playersSelect';
    gameSettingsPanel.appendChild(playersSelect);



    let createGameBtn = makeButton(parent=rightHomeScreen, text='Create Game', className='createGameBtn', callback=createGame);
    let findGameBtn = makeButton(parent=rightHomeScreen, text='Find Game', className='findGameBtn', callback=findGame);
}

function createDropDownSelect(options) {
    let select = document.createElement('select');

    //Create and append the options
    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.value = options[i];
        option.text = options[i];
        select.appendChild(option);
    }
    return select;
}

function generateTableHead(table, data =  {'id': '', 'level': '', 'speed': '', 'connections': ''}) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of Object.keys(data)) {
            if (key != 'connections') {
            let th = document.createElement("th");
            let text;
            text = document.createTextNode(key.substring(0, 1).toUpperCase() + key.substring(1));
            th.appendChild(text);
            row.appendChild(th);
        }
    }
}

function generateTable(table, data) {
    let body = table.createTBody();
    body.className = 'tableBody'
    for (let element of data) {
        let row = body.insertRow();

        row.onclick = joinGame.bind(null, element.id);  // bind function to click
        
        for (key in element) {
            let cell = row.insertCell();
            let text;
            if (key == 'players') {
                text = document.createTextNode(element.connections + '/' + element.players);let levelSelectLbl = document.createElement('label');
                levelSelectLbl.innerHTML = 'Choose Your Level:';
                cell.appendChild(text);
            } else if (key != 'connections') {
                text = document.createTextNode(element[key]); 
                cell.appendChild(text);
            } 
        }
    }
}

function displayGamePanel(games) {

    // Remove current table
    let oldTable = document.getElementById('gamesTable');
    oldTable.remove();

    // create a new table
    let gamesTable = document.createElement('table');
    gamesTable.className = 'gamesTable';
    gamesTable.id = 'gamesTable';

    document.getElementById('gamesPanel').appendChild(gamesTable);

    // Repopulate table
    if (games.length > 0) {    
        generateTableHead(gamesTable, games[0]);
    } else {
        generateTableHead(gamesTable);
    }
    generateTable(gamesTable, games);
}

function refreshGames() {
    send(new Query(AVAILABLE_GAMES));
}

/**
 * Creates a button on the parent element with given values
 * 
 * @param {*} parent 
 * @param {String} text 
 * @param {String} className 
 * @param {function} callback 
 * @returns 
 */
function makeButton(parent, text, className, callback) {
    var btn = document.createElement('button');
    btn.innerHTML = text;
    if (className) btn.className = className;
    if (callback) btn.onclick = callback;
    parent.appendChild(btn);
    return btn;
}

function joinGame(gameID) {
    document.location.href = '?join=' + gameID;
    // TODO: handle game joining
    send(new JoinGame(gameID));
}

function redirect(url) {
    const params = new URLSearchParams(window.location.search);
    alert('params: ' + params);
    if (params.has('join')) {
        alert('has join');
        document.body.removeChild(document.getElementsByClassName('homepage'));
    }
}

function createGame() {
    // Get dropdown elements
    let levelSelect = document.getElementById('levelSelect');
    let speedSelect = document.getElementById('speedSelect');
    let playersSelect = document.getElementById('playersSelect');

    // Get the values in the dropdown
    let level = levelSelect.options[levelSelect.selectedIndex].text;
    let speed = speedSelect.options[speedSelect.selectedIndex].text;
    let players = playersSelect.options[playersSelect.selectedIndex].text;
    
    // Tell server to create a new game
    send(new NewGame(level, speed, players));
    // Update game display
    send(new Query(AVAILABLE_GAMES));
}

function findGame() {
    send(new Message('Finding Game...'))
}

/**
 * Display board UI
 * 
 * @param {*} board 
 */
function createBoard() {
    // Create board div
    let board = document.createElement("div");
    board.className = "board";
    document.body.appendChild(board);

    //display piles
    const PILES = 5;
    const REALMS = 2;
    for (let realm = 0; realm < REALMS; realm++) {
        const realmElement = document.createElement("div");
        realmElement.className = "realm";
        realmElement.dataset.realm = realm;
        for (let pile = 0; pile < PILES; pile++) {
            const pileElement = document.createElement("div");
            pileElement.className = "pile";
            pileElement.dataset.pile = pile;
            pileElement.appendChild(createImage("C:/Users/Julian Walston/Documents/GitHub/scrimish/images/blue_card_back.png", imgClick));
            
            realmElement.append(pileElement);
        }
        board.append(realmElement);
    }
    return board;
}

/**
 * Create and return an image
 * 
 * @param {*} url 
 * @param {*} callback 
 * @returns 
 */
function createImage(src, callback) {
    var image = new Image();
    image.src = src;
    image.onclick = callback;
    image.width = 2.5 * IMAGE_SCALE;
    image.height = 3.5 * IMAGE_SCALE;
    return image;
}

/**
 * Event handler for clicks on card images
 */
function imgClick() {
    send(new Move(0, 3));
}

/**
 * Add an event handler to handle messages recieved from the server
 * 
 * @param {*} websocket 
 */
function recieveEvents(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data);
        console.log(event);
        if (event.type == 'joined game') {
            redirect('?join=' + event.id);

        } else if (event.type == AVAILABLE_GAMES) {
            displayGamePanel(event.data);
        } 
    });
}

/**
 * Send object to the server
 * 
 * @param {Event} event 
 */
function send(event) {
    if (websocket.readyState == 0) {
        websocket.onopen = () => websocket.send(JSON.stringify(event));
    } else {
        websocket.send(JSON.stringify(event));
    }
}

// class Game {
//     constructor (level, speed) {
//         this.level = level;
//         this.speed = speed;
//     }
// }

/**
 * Event Objects
 * events to pass to server
 */
class Event {
    type = '';
      constructor(type) {
        this.type = type;
      }
  }

class Move extends Event {
    attackPile;
    constructor(attackPile, defensePile) {
        super('move');
        this.attackPile = attackPile;
        this.defensePile = defensePile;
    }
}
  
class Message extends Event {
    text = '';
    constructor(text) {
        super('msg');
        this.text = text;
    }
}

class NewGame extends Event {
    constructor(level, speed, players) {
        super('new game');
        this.level = level;
        this.speed = speed;
        this.players = players;
    }
}

class JoinGame extends Event {
    id = '';
    constructor(id) {
        super('join');
        this.id = id;
    }
}

class Query extends Event {
    constructor(dataType) {
        super('query');
        this.dataType = dataType;
    }
}
