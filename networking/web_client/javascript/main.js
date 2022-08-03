// IMAGE GALLERY LINK = https://postimg.cc/gallery/SQmshss

var websocket;

const IMAGE_SCALE = 30;

const REALM_SIZE = 5;
const MAX_PILE_SIZE = 5;

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

let blueRealm = [];
let redRealm = [];
let userPlayerColor = "'r' or 'b'";

let selectedPile = -1;

let userID;
let gameID;

const USE_COOKIES = false;

// TODO - add game chat (with server messages)

window.addEventListener("DOMContentLoaded", () => {
    // Open WebSocket connection and register event handlers

    // websocket = new WebSocket("ws://localhost:8001/"); 
    
    websocket = new WebSocket(getWebSocketServer()); 

    


    recieveEvents(websocket);

    // Initialize the UI
    websocket.onopen = () => {
        console.log(document.cookie);
        if (USE_COOKIES) {
            userID = getCookie('userID'); // get the userID cookie if it exists
            send(new Connection(userID));
        } else {
            send(new Connection(''))
        }
        
        initUI();
    }

    // websocket.onclose = () => {
    //     send(new Disconnection());
    // }
});

function getWebSocketServer() {
    if (window.location.host === "https://julianrw1.github.io/scrimish/") {
      return "wss://scrimish.herokuapp.com/";
    } else if (window.location.host === "localhost:8000") {
      return "ws://localhost:8001/";
    } else {
      throw new Error(`Unsupported host: ${window.location.host}`);
    }
}

function initUI() {
    let params = new URLSearchParams(window.location.search);

    if (params.has('setup')) {
        initSetup(params.get('setup'));

    } else if (params.has('game')) {
        initGame(params.get('game'));

    } else {
        initHomepage();
    }
}

function initSetup(game_id) {
    gameID = game_id;

    if (!USE_COOKIES) {
        send(new ConnectToGame(gameID));
    }

    createSetupScreen(game_id);
}

function initGame(game_id) {

    gameID = game_id;

    
    if (!USE_COOKIES) {
        send(new ConnectToGame(gameID));
    }

    //display realms
    let initGameStateQuery = new Query('initialGameState');
    initGameStateQuery.gameID = gameID;
    send(initGameStateQuery);
}

function createSetupScreen() {

    let setUpScreen = document.createElement('div');
    setUpScreen.className = 'setupScreen';
    setUpScreen.id = 'setupScreen';
    document.body.appendChild(setUpScreen);

    let realmSetup = document.createElement('div');
    realmSetup.className = 'realmSetup';
    setUpScreen.appendChild(realmSetup);

    // let xOffset = 5;
    // let yOffset = 30;

    for (let pile = 0; pile < REALM_SIZE; pile++) {
        let setUpPileElement = document.createElement('div');
        setUpPileElement.className = 'setupPileElement';
        setUpPileElement.id = 'setupPile' + pile;
        realmSetup.appendChild(setUpPileElement);
        
        for (let card = 0; card < MAX_PILE_SIZE; card++) {

            let setUpCardElement = document.createElement('div');
            setUpCardElement.className = 'setupCardElement';

            setUpCardElement.ondragover = function (event) {
                allowDrop(event);
            }
            setUpCardElement.ondrop = function (event) {
                let img = document.getElementById(event.dataTransfer.getData('img'));
                if (!setUpCardElement.hasChildNodes()) {
                    drop(event);

                    if (!availableCardsQueue.hasChildNodes()) {
                        let continueToGameBtn = 
                                makeButton(setUpScreen, 'Continue', 'continueToGameBtn', continueToGame);
                        setUpScreen.appendChild(continueToGameBtn);
                    }
                }
            }
            setUpCardElement.id = 'cardslot' + "_" + pile + "_" + card;

            setUpPileElement.appendChild(setUpCardElement);
        }
    }
    let availableCardsQueue = document.createElement('div');
    availableCardsQueue.className = 'availableCardsSetup';
    setUpScreen.appendChild(availableCardsQueue);

    addCardsToQueue(availableCardsQueue);

    // TODO - temporary
    document.addEventListener('keyup', (e) => {
        if (e.code === "ArrowUp") {
            for (let i = 0; i < 25; i++) {
                let img = document.getElementById('img' + i);
                cardSlot = document.getElementById('cardslot_' + Math.floor(i/5) + '_' + (i % 5));
                cardSlot.appendChild(img);
            }
            //setup continue button
            let continueToGameBtn = makeButton(setUpScreen, 'Continue', 'continueToGameBtn', continueToGame);
            setUpScreen.appendChild(continueToGameBtn);
        }
    });


    setUpScreen.ondragover = function (event) {
        allowDrop(event);
    }

    setUpScreen.ondrop = function (event) {
        // if user drags card onto empty space place back in queue

        if (document.getElementById(event.dataTransfer.getData('img')) == event.target) {
            //don't return the element to the queue if it is dropped on its old square
            return;
        }
        
        var img = event.dataTransfer.getData("img");
        let imgElement = document.getElementById(img);


        if (event.target.className != 'setupCardElement') {
            // If the drop was not on a card slot
            availableCardsQueue.appendChild(imgElement);

            // Check if the "continue" button should be removed from screen
            setUpScreen.childNodes.forEach((childNode, key, parent) => {
                if (childNode.className == 'continueToGameBtn') {
                    childNode.remove();
                }
            });
        }

        
    }
}

function addCardsToQueue(queueElement) {
    const TOTAL_CARDS = [
        '1', '1', '1', '1', '1',
        '2', '2', '2', '2', '2',
        '3', '3', '3', 
        '4', '4', '4', 
        '5', '5', 
        '6', '6',
        'A', 'A', 
        'S', 'S', 
        'C'
    ];
    for (let card = 0; card < TOTAL_CARDS.length; card++) {
        // TODO: make based on player color
        let img = createImage(CARD_IMAGES['r' + '_' + TOTAL_CARDS[card]], 'setupCard', null);
        img.draggable = true;
        img.id = 'img' + card;
        img.ondragstart = function (event) {
            drag(event);
        }
        queueElement.appendChild(img);
    }
}

function allowDrop(ev) {
    ev.preventDefault();
}
  
function drag(ev) {
    ev.dataTransfer.setData("img", ev.target.id);
}
  
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("img");
    let img = document.getElementById(data);
    ev.target.appendChild(img);
}

function continueToGame() {


    // let realmData = new Data(gameID, 'realm', getUserCreatedRealm());
    // send(realmData);

    send(new ContinueToGame(gameID, getUserCreatedRealm()))


    // display realms
    // let initGameStateQuery = new Query('init game state');
    // initGameStateQuery.game_id = gameID;
    // send(initGameStateQuery); 
}

/**
 * Extracts the card order from the setup screen
 * @returns a 2D str array of the card order 
 */
function getUserCreatedRealm() {
    let realm = Array.from(Array(REALM_SIZE), () => new Array(MAX_PILE_SIZE));
    for (let pile = 0; pile < REALM_SIZE; pile++) {
        for (let cardSlot = 0; cardSlot < MAX_PILE_SIZE; cardSlot++) {
            let cardSlotElement = document.getElementById("cardslot_" + pile + "_" + (MAX_PILE_SIZE - cardSlot - 1));
            let cardImage = cardSlotElement.getElementsByTagName('img')[0];
            switch (cardImage.getAttribute("src")) {
                case CARD_IMAGES['r_1']:
                    realm[pile][cardSlot] = '1';
                    break;
                case CARD_IMAGES['r_2']:
                    realm[pile][cardSlot] = '2';
                    break;
                case CARD_IMAGES['r_3']:
                    realm[pile][cardSlot] = '3';
                    break;
                case CARD_IMAGES['r_4']:
                    realm[pile][cardSlot] = '4';
                    break;
                case CARD_IMAGES['r_5']:
                    realm[pile][cardSlot] = '5';
                    break;
                case CARD_IMAGES['r_6']:
                    realm[pile][cardSlot] = '6';
                    break;
                case CARD_IMAGES['r_A']:
                    realm[pile][cardSlot] = 'A';
                    break;
                case CARD_IMAGES['r_S']:
                    realm[pile][cardSlot] = 'S';
                    break;
                case CARD_IMAGES['r_C']:
                    realm[pile][cardSlot] = 'C';
                    break;
            }
        }
    }
    return realm;
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

    // Query the server for the available games when socket opens
    let sent = false;
    while (!sent) {
        
        if (websocket.readyState == 1) {
            //websocket is open
            send(new Query(AVAILABLE_GAMES)); 
            sent = true;
        }
    }
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
    if (userPlayerColor == 'b') {
        realmOrder = [redRealm, blueRealm]
    } else if (userPlayerColor == 'r') {
        realmOrder = [blueRealm, redRealm]
    }

    for (let realm = 0; realm < realmOrder.length; realm++) {
        let currentRealm = realmOrder[realm];

        const realmElement = document.createElement("div");
        
        let realmColor = ''; // 'r' or 'b'
            if (currentRealm == blueRealm) {
                realmColor = 'b';
            } else {
                realmColor = 'r';
            }

        realmElement.id = 'realm_' + realmColor;
        realmElement.className = "realm";
            
        for (let pile = 0; pile < currentRealm.length; pile++) {
            const pileElement = document.createElement("div");
            pileElement.className = "pile";
            pileElement.id = realmColor + '_pile_' + pile;
            

            if (currentRealm[pile].length != 0) {
                // let topCard = currentRealm[pile][currentRealm[pile].length - 1];
                imgPath = CARD_IMAGES[realmColor + '_back'];

                img = createImage(imgPath, 'card', cardClick.bind(null, pile, realmColor));
                img.id = pileElement.id + '_img';

                pileElement.appendChild(img);

                realmElement.appendChild(pileElement);
            }
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
function createImage(src, className, callback) {
    var image = new Image();
    image.src = src;
    if (callback != null) {
        image.onclick = callback;
    }
    image.className = className;
    return image;
}

/**
 * Event handler for clicks on card images
 */
function cardClick(pile, realmColor) {

    let cardRealm = 'none';
    if (realmColor == 'b') {
        cardRealm = blueRealm;
    } else if (realmColor == 'r') {
        cardRealm = redRealm;
    }
    let topCard = cardRealm[pile][cardRealm[pile].length - 1];

    let pileElement = document.getElementById(realmColor + '_pile_' + pile);

    let cardAlliance = topCard.substring(0,1) // 'r' or 'b'

    if (selectedPile == -1) {
        // No selected pile
        if (userPlayerColor == cardAlliance) {
            // Card belongs to player

            // select the clicked card
            flipCard(true, pile, topCard);
            selectedPile = pile;
        } 
    } else if (cardAlliance != userPlayerColor) {
        // Card belongs to opponent

        // perform attack
        send(new Attack(selectedPile, pile, userPlayerColor));

    } else if (pile == selectedPile && userPlayerColor == cardAlliance) {
        // card is already selected

        // deselect card
        flipCard(false, pile, topCard);
        selectedPile = -1;
    } else {
        // Card is own card

        //switch selected pile
        flipCard(false, selectedPile, topCard);
        flipCard(true, pile, topCard);
        selectedPile = pile;
    }
}

/**
 * 
 * @param {boolean} faceUp 
 */
function flipCard(faceUp, pile, topCard) {
    let realmColor = topCard.substring(0,1);

    let currentImage = document.getElementById(realmColor + '_pile_' + pile + '_img');

    if (faceUp) {
        // Get the current image
        currentImage.src = CARD_IMAGES[topCard];
    } else {
        currentImage.src = CARD_IMAGES[realmColor + '_back'];
    }

}

async function attack(attack_event) {
    // attack_event = {player_color, att_pile, def_pile, losers}
    let playerColor = attack_event.player_color;
    let attPile = attack_event.att_pile;
    let defPile = attack_event.def_pile;
    let losers = attack_event.losers;

    let activeRealm
    let inactiveRealm
    if (playerColor == 'r') {
        activeRealm = redRealm;
        inactiveRealm = blueRealm;
    } else if (playerColor == 'b') {
        activeRealm = blueRealm;
        inactiveRealm = redRealm;
    } else {
        throw 'in main.js - attack(): invalid player color';
    }

    let attCard = activeRealm[attPile][activeRealm[attPile].length - 1];
    let defCard = inactiveRealm[defPile][inactiveRealm[defPile].length - 1];

    // TODO - maybe animation?

    // flip any previusly selected cards down
    if (selectedPile != -1) {
        let selectedCard = activeRealm[selectedPile][activeRealm[selectedPile].length - 1];
        flipCard(false, selectedPile, selectedCard);
    }

    // flip attacker and defender
    flipCard(true, attPile, attCard);
    flipCard(true, defPile, defCard);
    
    // wait 
    await pause(2);

    // flip losers
    losers.forEach((loser) => {
        let loserPile;
        let loserRealm;
        let loserColor;

        if (loser == attCard) {
            loserPile = attPile;
            loserRealm = activeRealm;
            loserColor = attCard.substring(0,1);
        } else {
            loserPile = defPile;
            loserRealm = inactiveRealm;
            loserColor = defCard.substring(0,1);
        }

        loserRealm[loserPile].pop();

        if (loserRealm[loserPile].length != 0) {
            flipCard(false, loserPile, loser)
            
        } else {
            let pileElement = document.getElementById(loserColor + '_pile_' + loserPile);
            pileElement.remove();
            return;
        }

    })

    
    // wait 
    await pause(1);

    // flip winner
    if (activeRealm[attPile].length != 0) {
        flipCard(false, attPile, attCard);
    }
    if (inactiveRealm[defPile].length != 0) {
        flipCard(false, defPile, defCard);
    }
    
    // reset display
    selectedPile = -1;
}

function pause(seconds) {
    return new Promise(r => setTimeout(r, seconds * 1000));
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

        } else if (event.type == 'set') {
            if (event.variable == 'userID') {
                if (USE_COOKIES) {
                    setCookie('userID', event.value, false, 0);
                }
            } else if (event.variable == 'playerColor') {
                userPlayerColor = event.value;
            }

        } else if (event.type == 'attack') {
            attack(event);

        } else if (event.type == AVAILABLE_GAMES) {
            displayGamePanel(event.data);
            
        } else if (event.type == 'redirect') {
            document.location.href = event.url;

        } else if (event.type == 'lose') {
            // TODO - win message
            if (event.player != userPlayerColor) {
                alert('You win!')
            } else {
                alert('You lose.')
            }

        } 
        else if (event.type == 'continueToGame') {
            if (event.firstOrSecond == 'first') {
                // TODO: Go to a wait screen
            } 
        } 
        else if (event.type == 'initialGameState') {

            userPlayerColor = event.playerColor;
            
            // TODO: wait for both players to create a realm.
            redRealm = event.redRealm;
            blueRealm = event.blueRealm;

            createBoard();
        } else if (event.type == 'message') {
            // TODO: banner across top
            alert(event.text)
        } else {
            send(new Message('invalid type error [' + event.type + ']'))
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
 * 
 * @param {String} cname 
 * @param {*} cvalue 
 * @param {boolean} expirationDate 
 * @param {int} exdays 
 */
function setCookie(cname, cvalue, expirationDate, exdays) {
    if (expirationDate) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    } else {
        document.cookie = cname + '=' + cvalue + ';' + 'path=/';
    }
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
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

class Attack extends Event {
    attackPile;
    defensePile;
    playerColor;
    game_id;
    constructor(attackPile, defensePile, playerColor) {
        super('attack');
        this.game_id = gameID;
        this.attackPile = attackPile;
        this.defensePile = defensePile;
        this.playerColor = playerColor;
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

class ContinueToGame extends Event {
    constructor(id, realm) {
        super('continueToGame');
        this.id = id;
        this.realm = realm;
    }
}

class Data extends Event {
    constructor(gameID, dataType, data) {
        super('data');
        this.dataType = dataType;
        this.data = data;
        this.gameID = gameID;
    }
}

class ConnectToGame extends Event {
    constructor(gameID) {
        super('connectToGame');
        this.id = gameID;
    }
}

class Query extends Event {
    constructor(dataType) {
        super('query');
        this.dataType = dataType;
    }
}

class Connection extends Event {
    constructor(userID) {
        super('connection');
        this.userID = userID;
    }
}

class Disconnection extends Event {
    constructor(userID) {
        super('disconnection');
        this.userID = userID;
    }
}

//TODO - Disconnect event (more accurate than server side attempt)
