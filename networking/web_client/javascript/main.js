var websocket;

const IMAGE_SCALE = 50;

var activeGames = [];

const AVAILABLE_GAMES = 'available games';


window.addEventListener("DOMContentLoaded", () => {
    // Open WebSocket connection and register event handlers
    websocket = new WebSocket("ws://192.168.1.17:8001/"); 

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

    let leftHomeScreen = document.createElement('div');
    leftHomeScreen.className = 'leftHomeScreen';
    homepagePanel.appendChild(leftHomeScreen);

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

    let games = [
        new Game('jk11', 'Beginner', 'Slow'),
        new Game('ok56', 'Expert', 'Fast'),
        new Game('3kkl', 'Intermediate', 'Slow'),
        new Game('0op5', 'Intermediate', 'Very Fast'),
        new Game('asdf', 'Beginner', 'Slow'),
        new Game('lkjl', 'Expert', 'Fast'),
        new Game('hunt', 'Intermediate', 'Slow'),
        new Game('stir', 'Intermediate', 'Very Fast'),
        new Game('cars', 'Beginner', 'Slow'),
        new Game('okey', 'Expert', 'Fast'),
        new Game('akil', 'Intermediate', 'Slow'),
        new Game('0983', 'Intermediate', 'Very Fast'),
        new Game('1234', 'Beginner', 'Slow'),
        new Game('0000', 'Expert', 'Fast'),
        new Game('aaaa', 'Intermediate', 'Slow'),
        new Game('lilt', 'Intermediate', 'Very Fast')
    ];
    generateTableHead(gamesTable, games[0]);
    generateTable(gamesTable, games);

    refreshBtn = makeButton(parent=gameOptions, text='⟳ Refresh', className= 'refreshGamesBtn', refreshGames);

    websocket.onopen = () => send(new Query(AVAILABLE_GAMES));

    // create buttons panel
    let homepageBtnPanel = document.createElement('div');
    homepageBtnPanel.className = 'homepageBtnPanel';
    homepagePanel.appendChild(homepageBtnPanel).className;

    let createGameBtn = makeButton(parent=homepageBtnPanel, text='Create Game', className='createGameBtn', callback=createGame);
    let findGameBtn = makeButton(parent=homepageBtnPanel, text='Find Game', className='findGameBtn', callback=findGame);
}

function generateTableHead(table, data =  {'id': '', 'level': '', 'speed': '', 'connections': ''}) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of Object.keys(data)) {
        let th = document.createElement("th");
        let text;
        if (key == 'connections') {
            text = document.createTextNode('Players')
        } else {
            text = document.createTextNode(key.substring(0, 1).toUpperCase() + key.substring(1));
        }
        th.appendChild(text);
        row.appendChild(th);
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
            if (key == 'connections') {
                text = document.createTextNode(element.connections + '/' + 2);
            } else {
                text = document.createTextNode(element[key]);
            }
            //cell.style.color = 'white';
            cell.appendChild(text);
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
    send(new JoinGame(gameID));
}

function createGame() {
    send(new NewGame('Expert', 'Fast'));
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
        if (event.type == AVAILABLE_GAMES) {
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

class Game {
    constructor (level, speed) {
        this.level = level;
        this.speed = speed;
    }
}

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
    constructor(level, speed) {
        super('new game');
        this.level = level;
        this.speed = speed;
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
