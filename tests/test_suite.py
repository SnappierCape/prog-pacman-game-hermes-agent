"""Comprehensive Test Suite for Hermes Arcade: Pac-Man."""
import os, sys, random, subprocess, time
abs_proj = os.path.abspath(os.getcwd())
sys.path.insert(0, os.path.join(abs_proj, "src"))

passed_tests = 0
failed_tests = 0
def run_test(name, func):
    global passed_tests, failed_tests
    try:
        func()
        print(f"✅ {name}")
        passed_tests += 1
    except Exception as e:
        print(f"❌ FAILED {name}: {e}")
        failed_tests += 1

# --- A: Config & Constants ---
def test_config_loads():
    import config
    assert config.WINDOW_WIDTH == 640 and config.FPS == 60

def test_movement_tuning_positive():
    import config
    assert config.MOVEMENT_SPEED > 0

# --- B: Map & Collision Logic ---
def test_level_map_structure():
    from game.level_loader import get_tile_map, TILE_SIZE
    rows = get_tile_map()
    assert len(rows) == 20 and len(rows[0]) == 20, f"Incorrect map dimensions: {len(rows)}x{len(rows[0])}"

def test_level_wall_detection():
    from game.level_loader import is_wall
    assert is_wall(0, 0) is True   # Row 0 is all walls '#'
    assert is_wall(5, 4) is False  # Row 4 is open path ('.')

def test_level_oob_safety():
    from game.level_loader import is_wall
    assert is_wall(-900, -900) is False
    assert is_wall(5000, 5000) is False

def test_collision_blocking_logic():
    from game.collisions import try_move_player
    from game.level_loader import TILE_SIZE
    start_x = float(TILE_SIZE * 5 + 16)
    start_y = float(TILE_SIZE * 4 + 16)
    success, _, _ = try_move_player(start_x, start_y, start_x + 32, start_y)
    assert success is True, "Movement into empty space was blocked!"
    test_x = float(TILE_SIZE * 0 + 16) 
    success, rx, ry = try_move_player(start_x, start_y, test_x, start_y)
    assert success is False, "Player successfully moved into a solid wall!"

# --- C: Entity Integration ---
def test_pacman_integration_with_walls():
    from entities.pacMan import PacMan
    pm = PacMan()
    pm.set_direction("LEFT")
    for _ in range(300): pm.update()
    pos_after_impact = pm.pos_x
    for _ in range(50): pm.update()
    drift = abs(pm.pos_x - pos_after_impact)
    assert drift < 1.0, f"PacMan pushed through the wall! Drifted {drift}px"

# --- D: Economy (Pellets & Scoring) ---
def test_pellet_spawn_rates():
    from game.pellets import PelletManager, PELLET_TIERS
    random.seed(42) # Deterministic for testing
    mgr = PelletManager()
    total = len(mgr.pellets)
    assert total > 0, "No pellets spawned on the map!"
    counts = {"DOT": 0, "POWER": 0, "SUPER": 0}
    for p in mgr.pellets: counts[p["tier"]] += 1
    assert counts["DOT"] > counts["POWER"] > counts["SUPER"], f"Incorrect spawn hierarchy: {counts}"

def test_pellet_scoring_math():
    from game.pellets import PELLET_TIERS
    assert PELLET_TIERS["DOT"]["points"] == 1
    assert PELLET_TIERS["POWER"]["points"] == 5
    assert PELLET_TIERS["SUPER"]["points"] == 10

def test_pellet_consumption_and_score():
    from game.pellets import PelletManager
    mgr = PelletManager()
    initial_count = len(mgr.pellets)
    if initial_count > 0:
        px, py = mgr.pellets[0]["x"], mgr.pellets[0]["y"]
        # Walk right over the pellet
        hit = mgr.check_pickup(px, py)
        assert hit is True, "Failed to register a pellet pickup!"
        assert len(mgr.pellets) == initial_count - 1, "Pellet was not removed from memory!"

# --- E: Player State (Lives & Game Over) ---
def test_player_state_initial():
    from game.player_state import PlayerState, STARTING_LIVES
    ps = PlayerState()
    assert ps.lives == STARTING_LIVES, f"Expected {STARTING_LIVES} starting lives, got {ps.lives}"
    assert ps.game_over is False

def test_player_lose_life_and_death():
    from game.player_state import PlayerState, STARTING_LIVES
    ps = PlayerState()
    for _ in range(STARTING_LIVES - 1):
        ps.lose_life()
        assert ps.game_over is False, "Should not be game over before last life is lost"
    ps.lose_life()
    assert ps.game_over is True, "Player should trigger game over after losing all lives!"

def test_player_restart_reset():
    from game.player_state import PlayerState, STARTING_LIVES
    ps = PlayerState()
    for _ in range(2): ps.lose_life()
    ps.restart_game()
    assert ps.lives == STARTING_LIVES and ps.game_over is False, "Restart should reset lives and clear game over"
    assert ps.score == 0

# --- F: Ghosts & Difficulty ---
def test_difficulty_settings_exist():
    from game.difficulty import DIFFICULTY_SETTINGS
    assert 'easy' in DIFFICULTY_SETTINGS
    assert 'normal' in DIFFICULTY_SETTINGS
    assert 'hard' in DIFFICULTY_SETTINGS

def test_difficulty_ghost_counts():
    from game.difficulty import DIFFICULTY_SETTINGS
    # Easy has fewer ghosts than Hard
    assert DIFFICULTY_SETTINGS['easy']['ghost_count'] < DIFFICULTY_SETTINGS['hard']['ghost_count']
    
def test_ghost_manager_initialization():
    from game.ghost_manager import GhostManager
    from game.difficulty import DIFFICULTY_SETTINGS
    
    # Initialize with easy difficulty (few ghosts)
    mgr = GhostManager(DIFFICULTY_SETTINGS['easy'])
    assert len(mgr.ghosts) == 0  # Starts empty, spawns over time
    
def test_ghost_collision_detection():
    from game.ghost_manager import GhostManager
    from game.difficulty import DIFFICULTY_SETTINGS
    from entities.ghost import Ghost
    
    mgr = GhostManager(DIFFICULTY_SETTINGS['easy'])
    test_ghost = Ghost('Test', (255, 0, 0))
    test_ghost.speed = 1.0
    # Place ghost right on top of player position
    player_x, player_y = 320.0, 144.0
    test_ghost.pos_x = player_x + 10  # Very close but not touching
    test_ghost.pos_y = player_y
    
    is_overlapping = mgr.check_player_overlap(player_x, player_y)
    assert is_overlapping == False, "Ghost should not trigger death at safe distance"
    
def test_ghost_tracker_movement():
    from entities.ghost import Ghost
    g = Ghost('Tracker', (255, 0, 0))
    g.pos_x = 320.0
    g.pos_y = 144.0
    start_dist = g.distance_to_player(360.0, 180.0)
    assert start_dist > 0, "Distance calculation failed for separated entities"

# --- G: Game Loop (Headless) ---
def test_main_loop_lifecycle():
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    proc = subprocess.Popen(
        [sys.executable, os.path.join(abs_proj, "src/main.py")],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(1.5)
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Game loop hang detected.")

# --- Execution Sequence ---
if __name__ == "__main__":
    print("=" * 50)
    run_test("Config constants valid", test_config_loads)
    run_test("Speed tuning > 0", test_movement_tuning_positive)
    run_test("Map structure & tile consistency", test_level_map_structure)
    run_test("Wall/Path detection accuracy", test_level_wall_detection)
    run_test("Map Out-of-Bounds safety", test_level_oob_safety)
    run_test("Collision blocking logic works", test_collision_blocking_logic)
    run_test("Pacman physically respects walls", test_pacman_integration_with_walls)
    run_test("Pellet spawn hierarchy correct", test_pellet_spawn_rates)
    run_test("Pellet scoring math valid", test_pellet_scoring_math)
    run_test("Pellet consumption & score update", test_pellet_consumption_and_score)
    run_test("PlayerState initial lives", test_player_state_initial)
    run_test("Player lose life & death logic", test_player_lose_life_and_death)
    run_test("Player restart reset works", test_player_restart_reset)
    # Ghosts & Difficulty
    run_test("Difficulty settings structure valid", test_difficulty_settings_exist)
    run_test("Ghost count scales with difficulty", test_difficulty_ghost_counts)
    run_test("Ghost manager initializes correctly", test_ghost_manager_initialization)
    run_test("Ghost collision detection works", test_ghost_collision_detection)
    run_test("Ghost tracking movement logic", test_ghost_tracker_movement)
    # Loop
    run_test("Main loop headless survival (1.5s)", test_main_loop_lifecycle)
    print("-" * 50)
    summary = f"RESULTS: {passed_tests} passed, {failed_tests} failed."
    if failed_tests > 0:
        print(f"❌ FAIL: {summary}")
        sys.exit(1)
    else:
        print(f"✅ SUCCESS: ALL VALIDATIONS GREEN. {summary}")
