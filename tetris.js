const colors = [
  null,
  '#FF0D72',
  '#0DC2FF',
  '#0DFF72',
  '#F538FF',
  '#FF8E0D',
  '#FFE138',
  '#3877FF',
];

function createMatrix(w, h) {
  const matrix = [];
  while (h--) {
    matrix.push(new Array(w).fill(0));
  }
  return matrix;
}

function createPiece(type) {
  if (type === 'T') {
    return [
      [0, 0, 0],
      [1, 1, 1],
      [0, 1, 0],
    ];
  } else if (type === 'O') {
    return [
      [2, 2],
      [2, 2],
    ];
  } else if (type === 'L') {
    return [
      [0, 3, 0],
      [0, 3, 0],
      [0, 3, 3],
    ];
  } else if (type === 'J') {
    return [
      [0, 4, 0],
      [0, 4, 0],
      [4, 4, 0],
    ];
  } else if (type === 'I') {
    return [
      [0, 5, 0, 0],
      [0, 5, 0, 0],
      [0, 5, 0, 0],
      [0, 5, 0, 0],
    ];
  } else if (type === 'S') {
    return [
      [0, 6, 6],
      [6, 6, 0],
      [0, 0, 0],
    ];
  } else if (type === 'Z') {
    return [
      [7, 7, 0],
      [0, 7, 7],
      [0, 0, 0],
    ];
  }
}

function createPlayer(canvasId, scoreId) {
  const canvas = document.getElementById(canvasId);
  const context = canvas.getContext('2d');
  context.scale(20, 20);
  return {
    arena: createMatrix(12, 20),
    context,
    dropCounter: 0,
    dropInterval: 1000,
    pos: { x: 0, y: 0 },
    matrix: null,
    score: 0,
    scoreElement: document.getElementById(scoreId),
  };
}

function collide(arena, player) {
  const m = player.matrix;
  const o = player.pos;
  for (let y = 0; y < m.length; ++y) {
    for (let x = 0; x < m[y].length; ++x) {
      if (
        m[y][x] !== 0 &&
        (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0
      ) {
        return true;
      }
    }
  }
  return false;
}

function merge(arena, player) {
  player.matrix.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value !== 0) {
        arena[y + player.pos.y][x + player.pos.x] = value;
      }
    });
  });
}

function rotate(matrix, dir) {
  for (let y = 0; y < matrix.length; ++y) {
    for (let x = 0; x < y; ++x) {
      [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
    }
  }
  if (dir > 0) {
    matrix.forEach(row => row.reverse());
  } else {
    matrix.reverse();
  }
}

function playerDrop(player) {
  player.pos.y++;
  if (collide(player.arena, player)) {
    player.pos.y--;
    merge(player.arena, player);
    playerReset(player);
    arenaSweep(player);
    updateScore(player);
  }
  player.dropCounter = 0;
}

function playerMove(player, dir) {
  player.pos.x += dir;
  if (collide(player.arena, player)) {
    player.pos.x -= dir;
  }
}

function playerRotate(player, dir) {
  const pos = player.pos.x;
  let offset = 1;
  rotate(player.matrix, dir);
  while (collide(player.arena, player)) {
    player.pos.x += offset;
    offset = -(offset + (offset > 0 ? 1 : -1));
    if (offset > player.matrix[0].length) {
      rotate(player.matrix, -dir);
      player.pos.x = pos;
      return;
    }
  }
}

function playerReset(player) {
  const pieces = 'TJLOSZI';
  player.matrix = createPiece(pieces[(Math.random() * pieces.length) | 0]);
  player.pos.y = 0;
  player.pos.x =
    ((player.arena[0].length / 2) | 0) - ((player.matrix[0].length / 2) | 0);
  if (collide(player.arena, player)) {
    player.arena.forEach(row => row.fill(0));
    player.score = 0;
    updateScore(player);
  }
}

function arenaSweep(player) {
  let rowCount = 1;
  outer: for (let y = player.arena.length - 1; y > 0; --y) {
    for (let x = 0; x < player.arena[y].length; ++x) {
      if (player.arena[y][x] === 0) {
        continue outer;
      }
    }
    const row = player.arena.splice(y, 1)[0].fill(0);
    player.arena.unshift(row);
    ++y;
    player.score += rowCount * 10;
    rowCount *= 2;
  }
}

function drawMatrix(matrix, offset, ctx) {
  matrix.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value !== 0) {
        ctx.fillStyle = colors[value];
        ctx.fillRect(x + offset.x, y + offset.y, 1, 1);
      }
    });
  });
}

function draw() {
  players.forEach(player => {
    player.context.fillStyle = '#000';
    player.context.fillRect(0, 0, player.context.canvas.width, player.context.canvas.height);

    drawMatrix(player.arena, { x: 0, y: 0 }, player.context);
    drawMatrix(player.matrix, player.pos, player.context);
  });
}

function updateScore(player) {
  player.scoreElement.innerText = player.score;
}

const players = [
  createPlayer('player1', 'score1'),
  createPlayer('player2', 'score2'),
];

players.forEach(player => {
  playerReset(player);
  updateScore(player);
});

let lastTime = 0;
function update(time = 0) {
  const deltaTime = time - lastTime;
  lastTime = time;

  players.forEach(player => {
    player.dropCounter += deltaTime;
    if (player.dropCounter > player.dropInterval) {
      playerDrop(player);
    }
  });

  draw();
  requestAnimationFrame(update);
}

update();

document.addEventListener('keydown', event => {
  switch (event.code) {
    case 'ArrowLeft':
      playerMove(players[0], -1);
      break;
    case 'ArrowRight':
      playerMove(players[0], 1);
      break;
    case 'ArrowDown':
      playerDrop(players[0]);
      break;
    case 'ArrowUp':
      playerRotate(players[0], 1);
      break;
    case 'KeyA':
      playerMove(players[1], -1);
      break;
    case 'KeyD':
      playerMove(players[1], 1);
      break;
    case 'KeyS':
      playerDrop(players[1]);
      break;
    case 'KeyW':
      playerRotate(players[1], 1);
      break;
  }
});
