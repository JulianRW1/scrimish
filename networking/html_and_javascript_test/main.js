var websocket;


const IMAGE_SCALE = 50;

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI
    const board = document.querySelector(".board");
    createBoard(board);

    // Open WebSocket connection and register event handlers
    websocket = new WebSocket("ws://192.168.1.17:8001/"); 
    recieveMoves(board, websocket);
    sendMoves(board, websocket);
});

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

function createImage(url, callback) {
    var image = new Image();
    image.src = url;
    image.onclick = callback;
    image.width = 2.5 * IMAGE_SCALE;
    image.height = 3.5 * IMAGE_SCALE;
    return image;
}

/**
 * Send moves to server
 * @param {} baord 
 * @param {*} websocket 
 */
function sendMoves(board, websocket) {
    // Add event listeners
    move = {att_pile: 0, def_pile: 3};
    // Send event to websocket
    //websocket.send(JSON.stringify(move));
    websocket.onopen = () => websocket.send('hello');
}

function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
}

function recieveMoves(board, websocket) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data);
        console.log(event);
    });
}


document.body.style.background = "Gray";

var button = document.createElement("button");
button.innerHTML = "Add Card";
button.onclick = myFunc;
document.body.appendChild(button);


function myFunc() {
    const card = document.createElement('div');
    card.className = 'card';
    img = createImage("C:/Users/Julian Walston/Documents/GitHub/scrimish/images/blue_card_back.png", imgClick);
    document.body.appendChild(img);
    //document.body.appendChild(createImage("C:/Users/Julian Walston/Documents/GitHub/scrimish/images/blue_card_back.png", imgClick));
    websocket.send('Button Pressed');
}

function imgClick() {
    alert("you clicked");
    websocket.send('Card Clicked')
}
