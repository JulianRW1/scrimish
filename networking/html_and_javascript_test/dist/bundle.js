(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// net = require('net');

// const client = new Socket();
// client.connect(5000, "192.168.0.128", function () {
//     console.log("connected");
//     client.write('Hello Server, love Client');
// });
// client.on('data', function (data) {
//     console.log('data recieved');
//     console.log(data.toString('utf-8'));
// });

document.body.style.background = "Gray";

var button = document.createElement("button");
button.innerHTML = "Click Me!";
button.onclick = myFunc;
document.body.appendChild(button);


function myFunc() {
    const IMAGE_SCALE = 50;

    var image = document.createElement("img");
    image.src = "C:/Users/Julian Walston/Documents/GitHub/scrimish/images/blue_card_back.png";
    image.onclick = imgClick;
    image.width = 2.5 * IMAGE_SCALE;
    image.height = 3.5 * IMAGE_SCALE;
    image.alt = "blue card back image";
    document.body.appendChild(image);
}

function imgClick() {
    console.log("kljlkj");
}

},{}]},{},[1]);
