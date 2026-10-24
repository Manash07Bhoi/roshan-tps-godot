extends Node
## ROSHAN TPS automated headless test suite.
##
## Run from the project root with:
##   godot --headless --path . res://tests/test_runner.tscn
##
## The process exit code is 0 when every test passes, 1 otherwise.
## Results are printed as "[PASS]" / "[FAIL]" lines so CI logs stay readable.

const MAIN_SCENE_PATH: String = "res://main/main.tscn"
const LEVEL_LOAD_TIMEOUT_SEC: float = 600.0

var _passed: int = 0
var _failed: int = 0


func _ready() -> void:
	print("ROSHAN TPS test suite — Godot ", Engine.get_version_info().string)
	print("Physics server: ", PhysicsServer3D.get_class(),
			" | project setting physics/3d/physics_engine = ",
			ProjectSettings.get_setting("physics/3d/physics_engine"))
	_run.call_deferred()


func _run() -> void:
	test_all_resources_load()
	test_input_actions_used_by_scripts_exist()
	test_settings_defaults_complete()
	test_settings_ssao_and_ssil_mapping()
	test_branding_text()
	await test_gameplay_smoke()

	print("")
	print("RESULT: %d passed, %d failed" % [_passed, _failed])
	get_tree().quit(0 if _failed == 0 else 1)


func check(condition: bool, name: String, detail: String = "") -> void:
	if condition:
		_passed += 1
		print("[PASS] ", name)
	else:
		_failed += 1
		print("[FAIL] ", name, ("  -> " + detail) if detail != "" else "")


# --------------------------------------------------------------------------
# Static / resource checks
# --------------------------------------------------------------------------

func _collect_files(dir_path: String, extensions: PackedStringArray, out: PackedStringArray) -> void:
	var dir := DirAccess.open(dir_path)
	if dir == null:
		return
	dir.list_dir_begin()
	var entry: String = dir.get_next()
	while entry != "":
		if entry.begins_with("."):
			entry = dir.get_next()
			continue
		var full: String = dir_path.path_join(entry)
		if dir.current_is_dir():
			_collect_files(full, extensions, out)
		elif entry.get_extension() in extensions:
			out.append(full)
		entry = dir.get_next()
	dir.list_dir_end()


## Every scene, script and text resource in the project must load without error.
## This catches broken ext_resource paths, missing dependencies and GDScript
## parse errors in one pass.
func test_all_resources_load() -> void:
	var files := PackedStringArray()
	_collect_files("res://", PackedStringArray(["tscn", "tres", "gd", "gdshader"]), files)
	var broken := PackedStringArray()
	for path in files:
		var res: Resource = ResourceLoader.load(path)
		if res == null:
			broken.append(path)
		elif res is GDScript and not (res as GDScript).can_instantiate():
			broken.append(path + " (script cannot instantiate)")
	check(files.size() > 0 and broken.is_empty(),
			"All %d scenes/scripts/resources load" % files.size(), ", ".join(broken))


## Every input action referenced from GDScript must exist in the project InputMap,
## otherwise the control silently does nothing.
func test_input_actions_used_by_scripts_exist() -> void:
	var scripts := PackedStringArray()
	_collect_files("res://", PackedStringArray(["gd"]), scripts)
	var regex := RegEx.new()
	regex.compile("(?:is_action_(?:just_)?(?:pressed|released)|get_action_strength|action_press|action_release)\\(\\s*&?\"([a-z_]+)\"")
	var missing := PackedStringArray()
	var seen := {}
	for path in scripts:
		if path.begins_with("res://tests/"):
			continue
		var source: String = FileAccess.get_file_as_string(path)
		for m in regex.search_all(source):
			var action: String = m.get_string(1)
			seen[action] = true
			if not InputMap.has_action(action):
				missing.append(action + " (" + path + ")")
	check(seen.size() >= 10 and missing.is_empty(),
			"All %d input actions used by scripts exist in InputMap" % seen.size(), ", ".join(missing))


func test_settings_defaults_complete() -> void:
	var missing := PackedStringArray()
	for section in Settings.DEFAULTS:
		for key in Settings.DEFAULTS[section]:
			if not Settings.config_file.has_section_key(section, key):
				missing.append(section + "/" + key)
	check(missing.is_empty(), "Settings autoload populates every default key", ", ".join(missing))


## Regression test for the SSAO settings defect found during the baseline audit:
## selecting "Disabled" must actually disable SSAO (and SSIL), and both
## Medium/High must enable the effect.
func test_settings_ssao_and_ssil_mapping() -> void:
	var saved_ssao = Settings.config_file.get_value("rendering", "ssao_quality")
	var saved_ssil = Settings.config_file.get_value("rendering", "ssil_quality")
	var scene_root := Node.new()
	add_child(scene_root)

	var cases := [
		[-1, false],
		[RenderingServer.ENV_SSAO_QUALITY_MEDIUM, true],
		[RenderingServer.ENV_SSAO_QUALITY_HIGH, true],
	]
	for c in cases:
		var env := Environment.new()
		Settings.config_file.set_value("rendering", "ssao_quality", c[0])
		Settings.config_file.set_value("rendering", "ssil_quality", c[0])
		Settings.apply_graphics_settings(get_window(), env, scene_root)
		check(env.ssao_enabled == c[1],
				"SSAO setting %d -> ssao_enabled == %s" % [c[0], c[1]],
				"got " + str(env.ssao_enabled))
		check(env.ssil_enabled == c[1],
				"SSIL setting %d -> ssil_enabled == %s" % [c[0], c[1]],
				"got " + str(env.ssil_enabled))

	scene_root.queue_free()
	Settings.config_file.set_value("rendering", "ssao_quality", saved_ssao)
	Settings.config_file.set_value("rendering", "ssil_quality", saved_ssil)


## The personal branding is text-only; verify the player-facing strings.
func test_branding_text() -> void:
	check(ProjectSettings.get_setting("application/config/name") == "ROSHAN TPS",
			"Window/application title is ROSHAN TPS",
			str(ProjectSettings.get_setting("application/config/name")))
	var menu: Node = (load("res://menu/menu.tscn") as PackedScene).instantiate()
	var loading_label: Label = menu.get_node(^"UI/Loading/Label")
	check(loading_label.text.contains("ROSHAN TPS"), "Loading screen text shows ROSHAN TPS", loading_label.text)
	menu.free()


# --------------------------------------------------------------------------
# Headless gameplay smoke test (real scenes, real physics, simulated input)
# --------------------------------------------------------------------------

func _wait_physics(frames: int) -> void:
	for i in frames:
		await get_tree().physics_frame


func _find_level(main: Node) -> Node:
	for child in main.get_children():
		if child.has_node(^"SpawnedNodes"):
			return child
	return null


func test_gameplay_smoke() -> void:
	var main: Node = (load(MAIN_SCENE_PATH) as PackedScene).instantiate()
	main.name = "main"
	add_child(main)

	# In headless mode the menu starts a local session automatically (upstream behaviour),
	# which exercises the real threaded level-loading path.
	var start_ms: int = Time.get_ticks_msec()
	var level: Node = null
	while level == null and Time.get_ticks_msec() - start_ms < LEVEL_LOAD_TIMEOUT_SEC * 1000.0:
		await get_tree().process_frame
		level = _find_level(main)
	check(level != null, "Menu -> level transition completes",
			"level not loaded after %d s" % LEVEL_LOAD_TIMEOUT_SEC)
	if level == null:
		return
	print("       level loaded in %.1f s" % ((Time.get_ticks_msec() - start_ms) / 1000.0))

	var spawned: Node = level.get_node(^"SpawnedNodes")
	await _wait_physics(5)
	var player: CharacterBody3D = spawned.get_node_or_null(^"1")
	check(player != null, "Local player spawned")
	if player == null:
		return

	var robots: Array = spawned.get_children().filter(func(n): return n.has_signal(&"exploded"))
	check(robots.size() > 0, "Enemy robots spawned (%d)" % robots.size())

	# Let the player settle onto the floor.
	var settle := 0
	while not player.is_on_floor() and settle < 240:
		await get_tree().physics_frame
		settle += 1
	check(player.is_on_floor(), "Player lands on the floor (collision with level)")

	var player_input: Node = player.get_node(^"InputSynchronizer")

	# Movement.
	var start_pos: Vector3 = player.global_position
	Input.action_press(&"move_forward")
	await _wait_physics(60)
	Input.action_release(&"move_forward")
	var moved: float = Vector2(player.global_position.x - start_pos.x,
			player.global_position.z - start_pos.z).length()
	check(moved > 0.5, "Forward input moves the player", "moved %.3f m" % moved)
	await _wait_physics(30)

	# Jump.
	var ground_y: float = player.global_position.y
	var max_y: float = ground_y
	Input.action_press(&"jump")
	await get_tree().process_frame
	await get_tree().process_frame
	Input.action_release(&"jump")
	for i in 40:
		await get_tree().physics_frame
		max_y = maxf(max_y, player.global_position.y)
	check(max_y - ground_y > 0.3, "Jump input lifts the player", "rise %.3f m" % (max_y - ground_y))
	settle = 0
	while not player.is_on_floor() and settle < 240:
		await get_tree().physics_frame
		settle += 1
	check(player.is_on_floor(), "Player lands again after jumping")

	# Camera look via a real mouse-motion event.
	var camera_base: Node3D = player.get_node(^"CameraBase")
	var yaw_before: Basis = camera_base.global_transform.basis
	var motion := InputEventMouseMotion.new()
	motion.relative = Vector2(300, 0)
	motion.screen_relative = Vector2(300, 0)
	Input.parse_input_event(motion)
	await get_tree().process_frame
	await get_tree().process_frame
	check(not camera_base.global_transform.basis.is_equal_approx(yaw_before), "Mouse motion rotates the camera")

	# Aim + shoot.
	Input.action_press(&"aim")
	await _wait_physics(10)
	check(player_input.aiming, "Aim input enters aiming mode")
	var bullets_before: int = _count_bullets(spawned)
	Input.action_press(&"shoot")
	await _wait_physics(20)
	Input.action_release(&"shoot")
	var bullets_after: int = _count_bullets(spawned)
	check(bullets_after > bullets_before, "Shooting while aiming spawns bullets",
			"%d -> %d" % [bullets_before, bullets_after])
	Input.action_release(&"aim")
	await _wait_physics(5)

	# Enemy damage and death logic.
	if robots.size() > 0:
		var robot: Node = robots[0]
		var exploded := [false]
		robot.exploded.connect(func(): exploded[0] = true)
		var hp: int = robot.health
		robot.hit()
		check(robot.health == hp - 1, "Enemy takes damage when hit")
		for i in hp - 1:
			robot.hit()
		check(robot.dead and exploded[0], "Enemy dies and emits 'exploded' at zero health")

	# Quit back to menu (Escape / gamepad Start).
	# level.gd handles quit in _input(), so a real InputEvent must be dispatched.
	var quit_event := InputEventAction.new()
	quit_event.action = &"quit"
	quit_event.pressed = true
	Input.parse_input_event(quit_event)
	await get_tree().process_frame
	await get_tree().process_frame
	await get_tree().process_frame
	var back_in_menu: bool = false
	for child in main.get_children():
		if child.has_node(^"UI/Main/Play"):
			back_in_menu = true
	check(back_in_menu, "Quit action returns to the main menu")
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	# In headless mode the menu immediately auto-hosts again (upstream behaviour) and
	# reloads the level; wait until that completes so we never exit mid-load.
	var wait_start: int = Time.get_ticks_msec()
	while _find_level(main) == null and Time.get_ticks_msec() - wait_start < 120000:
		await get_tree().process_frame
	check(_find_level(main) != null, "Second session starts after returning to menu (scene re-entry)")
	await _wait_physics(10)
	main.queue_free()
	await _wait_physics(5)


func _count_bullets(parent: Node) -> int:
	var n := 0
	for child in parent.get_children():
		var s: Script = child.get_script()
		if s != null and s.resource_path == "res://player/bullet/bullet.gd":
			n += 1
	return n
