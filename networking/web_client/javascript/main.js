// IMAGE GALLERY LINK = https://postimg.cc/gallery/SQmshss

var websocket;

const IMAGE_SCALE = 50;

var activeGames = [];

const AVAILABLE_GAMES = 'available games';

const CARD_IMAGES = {
    'r_back': 'https://i.postimg.cc/43y9Kh7D/red-card-back.png',
    'r_1': 'https://i.postimg.cc/j5Jnc0hv/red-dagger.png',
    'r_2': 'https://i.postimg.cc/hP0zp09F/red-sw-ord.png',
    'r_3': 'https://i.postimg.cc/44VhhGyx/red-morning-star.png',
    'r_4': 'https://i.postimg.cc/wjTtPsV1/red-war-axe.png',
    'r_5': 'https://i.postimg.cc/zvZbPttN/red-halberd.png',
    'r_6': 'https://i.postimg.cc/wMXyKXZm/red-longsw-ord.png',
    'r_A': 'https://i.postimg.cc/9QJ9FBMP/red-archer.png',
    'r_S': 'https://i.postimg.cc/Fsvky6kg/red-shield.png',
    'r_C': 'https://i.postimg.cc/s2LZ5D5v/red-crown.png',
    'b_back': 'https://i.postimg.cc/D0LsvkJm/blue-card-back.png',
    'b_1': 'https://i.postimg.cc/Nj462cNH/blue-dagger.png',
    'b_2': 'https://i.postimg.cc/vHwfPBkn/blue-sw-ord.png',
    'b_3': 'https://i.postimg.cc/LXrLF6sr/blue-morning-star.png',
    'b_4': 'https://i.postimg.cc/3JjpzhQc/blue-war-axe.png',
    'b_5': 'https://i.postimg.cc/BvnxxVyw/blue-halberd.png',
    'b_6': 'https://i.postimg.cc/bJGk52qx/blue-longsw-ord.png',
    'b_A': 'https://i.postimg.cc/g2dy0JKp/blue-archer.png',
    'b_S': 'https://i.postimg.cc/QNTck54s/blue-shield.png',
    'b_C': 'https://i.postimg.cc/1z7DMK1R/blue-crown.png'
};

let blueRealm = []
let redRealm = []
let userPlayerColor = 'White'


window.addEventListener("DOMContentLoaded", () => {
    // Open WebSocket connection and register event handlers
    // websocket = new WebSocket("ws://192.168.1.17:8001/"); 
    websocket = new WebSocket("ws://localhost:8001/"); 

    recieveEvents(websocket);

    // Initialize the UI
    initUI();

    // board = createBoard();

});

function initUI() {
    let params = new URLSearchParams(window.location.search);
    if (params.has('game')) {
        initGame(params.get('game'));
    } else {
        initHomepage();
    }
}

function initGame(game_id) {

    let initGameStateQuery = new Query('init game state')
    initGameStateQuery.game_id = game_id
    send(initGameStateQuery)
}

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

    let playersSelect = createDropDownSelect([2]);
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

function generateTableHead(table, data =  {'id': '', 'level': '', 'speed': ''}) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of Object.keys(data)) {
        let th = document.createElement("th");
        let text;
        text = document.createTextNode(key.substring(0, 1).toUpperCase() + key.substring(1));
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
    // TODO: handle game joining
    send(new JoinGame(gameID));
}

function createGame() {
    // Get dropdown elements
    let levelSelect = document.getElementById('levelSelect');
    let speedSelect = document.getElementById('speedSelect');
    let playersSelect = document.getElementById('playersSelect');

    // Get the values in the dropdown
    let level = levelSelect.options[levelSelect.selectedIndex].text;
    let speed = speedSelect.options[speedSelect.selectedIndex].text;
    
    // Tell server to create a new game
    send(new NewGame(level, speed));
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
    

    let realmOrder = []
    if (userPlayerColor == 'Blue') {
        realmOrder = [redRealm, blueRealm]
    } else if (userPlayerColor == 'Red') {
        realmOrder = [blueRealm, redRealm]
    }

    for (let realm = 0; realm < realmOrder.length; realm++) {
        let currentRealm = realmOrder[realm];

        const realmElement = document.createElement("div");
        realmElement.className = "realm";
        realmElement.dataset.realm = realm;
            
        for (let pile = 0; pile < currentRealm.length; pile++) {
            const pileElement = document.createElement("div");
            pileElement.className = "pile";
            pileElement.dataset.pile = pile;

            let topCard = currentRealm[pile][currentRealm[pile].length - 1]
            imgPath = CARD_IMAGES[topCard];

            img = createImage(imgPath, IMAGE_SCALE, cardClick.bind(null, pile, topCard));

            pileElement.appendChild(img);

            realmElement.appendChild(pileElement);
        }
        board.append(realmElement);
    };
}

/**
 * Create and return an image
 * 
 * @param {*} url 
 * @param {*} callback 
 * @returns 
 */
function createImage(src, img_scale, callback) {
    var image = new Image();
    image.src = src;
    image.onclick = callback;
    image.width = 2.5 * img_scale;
    image.height = 3.5 * img_scale;
    return image;
}

/**
 * Event handler for clicks on card images
 */
function cardClick(pile, card) {

    alert('pile: ' + pile)
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
            send(new Message('joined game'));

        } else if (event.type == AVAILABLE_GAMES) {
            displayGamePanel(event.data);
            
        } else if (event.type == 'redirect') {
            document.location.href = event.url;

        } else if (event.type == 'init game state') {
            redRealm = event.redRealm;
            blueRealm = event.blueRealm;

            createBoard();
        } else if (event.type = 'player color') {
            userPlayerColor = event.color;
        } else {
            send(new Message('invalid type [ERROR]'))
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

//TODO - Disconnect event (more accurate than server side attempt)
