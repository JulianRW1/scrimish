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

export class Message extends Event {
  text = '';
  constructor(text) {
      super('msg');
      this.text = text;
  }
}