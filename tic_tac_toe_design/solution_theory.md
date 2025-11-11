# Tic-Tac-Toe Game Design - Solution Theory: Bottom-Up Approach

## Functional Requirements:
---------------------------
1. The Tic-Tac-Toe game should be played on a N*N grid.
2. Both players will choose their symbol.
3. Players take turns to make moves.
4. A player wins if they have N symbols in a row (horizontal, vertical, or
   diagonal).
5. The game ends when a player wins or the grid is full (draw).
6. Players can select the grid size (N*N) at the start of the game.
7. Players can choose their symbols (must be different).

## Entities:
-----------
- Grid: Represents the game board
- Symbol: Represents player symbols
- Player: Represents a game player
- Game: Manages game state and logic
- GameController: Orchestrates the game flow

## What is Bottom-Up Approach?
----------------------------
Bottom-Up approach means starting with the smallest, most basic components
and building up to more complex systems. We identify the fundamental building
blocks first, then combine them to create higher-level functionality.

## Step-by-Step Approach for Tic-Tac-Toe:
---------------------------------------

### STEP 1: Identify Core Primitives (Lowest Level)
------------------------------------------------
Start with the most basic, indivisible components:

1. **Symbol (Value Object)**
   - Purpose: Represents a single character symbol (X, O, or custom)
   - Why first: It's the most basic entity - everything else depends on it
   - Properties: Single character value
   - Methods: Basic getters, equality check

2. **GameStatus (Enum)**
   - Purpose: Represents possible game states
   - Why early: Needed by multiple components
   - Values: IN_PROGRESS, PLAYER_1_WON, PLAYER_2_WON, DRAW

### STEP 2: Build Basic Entities (Next Level)
------------------------------------------
Combine primitives to create basic entities:

3. **Player**
   - Purpose: Represents a game player
   - Depends on: Symbol
   - Properties: name, symbol
   - Methods: get_name(), get_symbol()

4. **Grid (Core Data Structure)**
   - Purpose: Represents the N*N game board
   - Depends on: Symbol (to store in cells)
   - Properties: size, 2D array of Symbols
   - Methods:
     * is_cell_empty(row, col)
     * place_symbol(row, col, symbol)
     * get_symbol(row, col)
     * is_full()
     * display()

### STEP 3: Build Business Logic Components
----------------------------------------
Add components that contain game logic:

5. **WinChecker (Strategy Pattern)**
   - Purpose: Check if a player has won
   - Depends on: Grid, Symbol
   - Why separate: Different win conditions (row, column, diagonal)
   - Components:
     * WinChecker (abstract interface)
     * RowWinChecker
     * ColumnWinChecker
     * DiagonalWinChecker

### STEP 4: Build Game Orchestration
---------------------------------
Combine entities and logic to create game flow:

6. **Game**
   - Purpose: Manages game state and rules
   - Depends on: Grid, Player, WinChecker, GameStatus
   - Properties: grid, player1, player2, current_player, status
   - Methods:
     * make_move(row, col) - Core game logic
     * get_current_player()
     * get_status()
     * _check_win() - Uses WinChecker strategies
     * _switch_player()

### STEP 5: Build Controller/Manager Layer
--------------------------------------
Create the top-level orchestrator:

7. **GameController**
   - Purpose: Orchestrates game flow and user interaction
   - Depends on: Game
   - Methods:
     * start_new_game() - Initializes game
     * make_move() - Delegates to Game
     * display_game() - Shows current state
     * get_game_status() - Gets current status
     * is_game_over() - Checks if game ended

### STEP 6: Build User Interface
----------------------------
Add user interaction layer:

8. **Helper Functions**
   - get_user_input() - Validates user input
   - validate_grid_size() - Validates grid size
   - validate_symbol() - Validates symbol

9. **Main Function**
   - Orchestrates entire game flow
   - Gets user input
   - Creates controller and game
   - Runs game loop
   - Handles game end

## Bottom-Up Building Order:
-------------------------
**Level 1 (Primitives):**
  Symbol → GameStatus

**Level 2 (Basic Entities):**
  Player (uses Symbol)
  Grid (uses Symbol)

**Level 3 (Logic Components):**
  WinChecker strategies (use Grid, Symbol)

**Level 4 (Game Logic):**
  Game (uses Grid, Player, WinChecker, GameStatus)

**Level 5 (Orchestration):**
  GameController (uses Game)

**Level 6 (Interface):**
  Helper functions + Main (use GameController)

## Benefits of Bottom-Up Approach:
-------------------------------
1. **Clear Dependencies**: Each level depends only on lower levels
2. **Testable**: Can test each component independently
3. **Reusable**: Lower-level components can be reused
4. **Maintainable**: Changes in one level don't affect others
5. **Understandable**: Build complexity gradually

## Key Design Principles Applied:
------------------------------
1. **Single Responsibility**: Each class has one job
2. **Dependency Inversion**: High-level depends on abstractions
3. **Strategy Pattern**: Win checking is pluggable
4. **Separation of Concerns**: UI, logic, and data are separated
5. **Encapsulation**: Internal state is protected

## Testing Strategy (Bottom-Up):
-----------------------------
1. Test Symbol class first (simplest)
2. Test Grid with Symbol
3. Test Player with Symbol
4. Test WinChecker strategies
5. Test Game with all components
6. Test GameController
7. Integration test with Main

## Summary:
---------
This approach ensures each component works correctly before building on top
of it, making debugging easier and code more reliable. The bottom-up approach
provides:

- ✅ Clear dependency hierarchy
- ✅ Independent testability
- ✅ Easy maintenance
- ✅ Gradual complexity building
- ✅ Reusable components

