var websocket;

const IMAGE_SCALE = 50;


window.addEventListener("DOMContentLoaded", () => {
    // Open WebSocket connection and register event handlers
    websocket = new WebSocket("ws://192.168.1.17:8001/"); 

    recieveEvents(websocket);
    
    // Initialize the UI
    initHomepage();

    board = createBoard();

});

function initHomepage() {
    // create games panel
    let openGamesPanel = document.createElement('div');
    openGamesPanel.className = 'openGamesPanel';
    document.body.appendChild(openGamesPanel);

    // create buttons panel
    let homepageBtnPanel = document.createElement('div');
    homepageBtnPanel.className = 'homepageBtnPanel';
    document.body.appendChild(homepageBtnPanel).className;

    let createGameBtn = makeButton(homepageBtnPanel, 'Create Game', 'createGameBtn', createGame);
}

function makeButton(parent, text, className, callback) {
    btn = document.createElement('button');
    btn.innerHTML = text;
    btn.className = className;
    btn.onclick = callback;
    parent.appendChild(btn);
    return btn;
}

function createGame() {
    send(new Message('game created'));
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
    });
}

/**
 * Send object to the server
 * 
 * @param {} event 
 */
function send(event) {
    websocket.send(JSON.stringify(event));
}

// Create button
var button = makeButton(document.body, "My Button", '', myFunc);

/**
 * Button handler (for testing)
 */
function myFunc() {
    send(new Message('Button Clicked'));
}


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
