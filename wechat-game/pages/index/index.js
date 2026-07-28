// 合成大正鹅 - 游戏核心逻辑
const SIZE = 4
const SAVE_KEY = 'dazheng-e-2048-save'
const BEST_KEY = 'dazheng-e-2048-best'

Page({
  data: {
    grid: [],
    tiles: [],
    score: 0,
    best: 0,
    scorePop: false,
    showOverlay: false,
    overlayTitle: '',
    overlaySubtitle: '',
    isWin: false,
    history: [],
    gameOver: false,
    won: false,
    isAnimating: false
  },

  touchStartX: 0,
  touchStartY: 0,

  onLoad() {
    this.loadGame()
  },

  // 加载存档
  loadGame() {
    const best = wx.getStorageSync(BEST_KEY) || 0
    const saved = wx.getStorageSync(SAVE_KEY)

    if (saved && saved.grid && saved.grid.length === SIZE) {
      this.setData({
        grid: saved.grid,
        score: saved.score || 0,
        best: best,
        history: saved.history || [],
        gameOver: saved.gameOver || false,
        won: saved.won || false
      })
      this.renderTiles()
    } else {
      this.startNewGame()
    }
  },

  // 开始新游戏
  startNewGame() {
    const grid = []
    for (let r = 0; r < SIZE; r++) {
      grid[r] = []
      for (let c = 0; c < SIZE; c++) {
        grid[r][c] = 0
      }
    }

    this.setData({
      grid,
      score: 0,
      history: [],
      gameOver: false,
      won: false,
      showOverlay: false
    })

    this.addRandomTile()
    this.addRandomTile()
    this.renderTiles()
    this.saveGame()
  },

  restart() {
    this.startNewGame()
  },

  // 撤销
  undo() {
    const { history, gameOver } = this.data
    if (history.length > 0 && !gameOver) {
      const prev = history[history.length - 1]
      this.setData({
        grid: prev.grid,
        score: prev.score,
        history: history.slice(0, -1),
        gameOver: false
      })
      this.renderTiles()
      this.saveGame()
    }
  },

  // 添加随机方块
  addRandomTile() {
    const { grid } = this.data
    const emptyCells = []

    for (let r = 0; r < SIZE; r++) {
      for (let c = 0; c < SIZE; c++) {
        if (grid[r][c] === 0) {
          emptyCells.push({ r, c })
        }
      }
    }

    if (emptyCells.length > 0) {
      const cell = emptyCells[Math.floor(Math.random() * emptyCells.length)]
      grid[cell.r][cell.c] = Math.random() < 0.9 ? 2 : 4
      this.setData({ grid })
      return cell
    }
    return null
  },

  // 触摸事件
  touchStart(e) {
    this.touchStartX = e.touches[0].clientX
    this.touchStartY = e.touches[0].clientY
  },

  touchMove(e) {
    // 阻止页面滚动
    e.preventDefault && e.preventDefault()
  },

  touchEnd(e) {
    const { gameOver, won, isAnimating } = this.data
    if (gameOver || won || isAnimating) return

    const touchEndX = e.changedTouches[0].clientX
    const touchEndY = e.changedTouches[0].clientY

    const dx = touchEndX - this.touchStartX
    const dy = touchEndY - this.touchStartY
    const absDx = Math.abs(dx)
    const absDy = Math.abs(dy)

    if (Math.max(absDx, absDy) < 30) return

    let direction
    if (absDx > absDy) {
      direction = dx > 0 ? 'right' : 'left'
    } else {
      direction = dy > 0 ? 'down' : 'up'
    }

    this.move(direction)
  },

  // 移动逻辑
  move(direction) {
    const { grid, score } = this.data
    const prevGrid = JSON.parse(JSON.stringify(grid))

    // 保存历史
    const history = [...this.data.history, { grid: prevGrid, score }]
    if (history.length > 5) history.shift()

    let moved = false
    const mergedPositions = []
    const traversals = this.getTraversals(direction)
    const merged = Array(SIZE).fill(0).map(() => Array(SIZE).fill(false))

    traversals.rows.forEach(r => {
      traversals.cols.forEach(c => {
        const value = grid[r][c]
        if (value === 0) return

        const result = this.findFarthestPosition(r, c, direction, merged)

        if (result.canMerge && grid[result.newR][result.newC] === value) {
          grid[r][c] = 0
          grid[result.newR][result.newC] = value * 2
          merged[result.newR][result.newC] = true
          mergedPositions.push({ r: result.newR, c: result.newC })
          moved = true
        } else if (result.newR !== r || result.newC !== c) {
          grid[r][c] = 0
          grid[result.newR][result.newC] = value
          moved = true
        }
      })
    })

    if (moved) {
      this.setData({ isAnimating: true, history })
      this.renderTiles()

      setTimeout(() => {
        const newTile = this.addRandomTile()
        this.renderTiles(newTile, mergedPositions)
        this.updateScoreDisplay()

        setTimeout(() => {
          this.setData({ isAnimating: false })
          this.checkGameState()
          this.saveGame()
        }, 100)
      }, 100)
    } else {
      // 没有移动，不保存历史
      this.setData({ history: history.slice(0, -1) })
    }
  },

  getTraversals(direction) {
    const rows = [], cols = []
    for (let i = 0; i < SIZE; i++) {
      rows.push(i)
      cols.push(i)
    }
    if (direction === 'down') rows.reverse()
    if (direction === 'right') cols.reverse()
    return { rows, cols }
  },

  getVector(direction) {
    switch (direction) {
      case 'up': return { r: -1, c: 0 }
      case 'down': return { r: 1, c: 0 }
      case 'left': return { r: 0, c: -1 }
      case 'right': return { r: 0, c: 1 }
    }
  },

  findFarthestPosition(r, c, direction, merged) {
    const vector = this.getVector(direction)
    const value = this.data.grid[r][c]
    let newR = r, newC = c

    while (true) {
      const nextR = newR + vector.r
      const nextC = newC + vector.c

      if (nextR < 0 || nextR >= SIZE || nextC < 0 || nextC >= SIZE) break

      if (this.data.grid[nextR][nextC] === 0) {
        newR = nextR
        newC = nextC
      } else if (this.data.grid[nextR][nextC] === value && !merged[nextR][nextC]) {
        return { newR: nextR, newC: nextC, canMerge: true }
      } else {
        break
      }
    }

    return { newR, newC, canMerge: false }
  },

  // 更新分数
  updateScoreDisplay() {
    const { score } = this.data
    let { best } = this.data

    this.setData({ scorePop: true })
    setTimeout(() => this.setData({ scorePop: false }), 200)

    if (score > best) {
      best = score
      wx.setStorageSync(BEST_KEY, best)
      this.setData({ best })
    }
  },

  // 检查游戏状态
  checkGameState() {
    const { grid, score, won } = this.data

    if (!won) {
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          if (grid[r][c] === 2048) {
            this.setData({
              won: true,
              showOverlay: true,
              overlayTitle: '你赢了！',
              overlaySubtitle: '得分：' + score,
              isWin: true
            })
            return
          }
        }
      }
    }

    if (!this.canMove()) {
      this.setData({
        gameOver: true,
        showOverlay: true,
        overlayTitle: '游戏结束',
        overlaySubtitle: '最终得分：' + score,
        isWin: false
      })
    }
  },

  canMove() {
    const { grid } = this.data

    for (let r = 0; r < SIZE; r++) {
      for (let c = 0; c < SIZE; c++) {
        if (grid[r][c] === 0) return true
      }
    }

    for (let r = 0; r < SIZE; r++) {
      for (let c = 0; c < SIZE; c++) {
        const value = grid[r][c]
        if (r < SIZE - 1 && grid[r + 1][c] === value) return true
        if (c < SIZE - 1 && grid[r][c + 1] === value) return true
      }
    }

    return false
  },

  // 渲染方块
  renderTiles(newTilePos, mergedPositions) {
    const { grid } = this.data
    const tiles = []

    for (let r = 0; r < SIZE; r++) {
      for (let c = 0; c < SIZE; c++) {
        const value = grid[r][c]
        if (value === 0) continue

        const tile = { r, c, value }

        if (newTilePos && newTilePos.r === r && newTilePos.c === c) {
          tile.isNew = true
        }

        if (mergedPositions && mergedPositions.some(p => p.r === r && p.c === c)) {
          tile.isMerged = true
        }

        tiles.push(tile)
      }
    }

    this.setData({ tiles })
  },

  // 保存游戏
  saveGame() {
    const { grid, score, history, gameOver, won } = this.data
    wx.setStorageSync(SAVE_KEY, {
      grid,
      score,
      history: history.slice(-4),
      gameOver,
      won
    })
  }
})
