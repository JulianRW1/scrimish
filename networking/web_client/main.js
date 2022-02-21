var websocket;

const IMAGE_SCALE = 50;


window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI
    const board = document.querySelector(".board");
    createBoard(board);

    // Open WebSocket connection and register event handlers
    websocket = new WebSocket("ws://192.168.1.17:8001/"); 

    recieveEvents(websocket);
});

/**
 * Display board UI
 * 
 * @param {*} board 
 */
function createBoard(board) {

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
    move = {type: "move", att_pile: 0, def_pile: 3};
    send(move);
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
var button = document.createElement("button");
button.innerHTML = "Add Card";
button.onclick = myFunc;
document.body.appendChild(button);

/**
 * Button handler (for testing)
 */
function myFunc() {
    send({type :"msg", text: 'Button Clicked!'});
}
