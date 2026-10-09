<?php
/**
 * Mission Board v2.2 - Simplified columns + Mission Banner
 * URL: https://sellmyhousefastbrevardfl.com/mb/
 * Auth: mp / 1317
 */

$valid_user = 'mp';
$valid_pass = '1317';

if (!isset($_SERVER['PHP_AUTH_USER']) ||
    $_SERVER['PHP_AUTH_USER'] !== $valid_user ||
    $_SERVER['PHP_AUTH_PW'] !== $valid_pass) {
    header('WWW-Authenticate: Basic realm="Mission Board"');
    header('HTTP/1.0 401 Unauthorized');
    header('Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate');
    header('Pragma: no-cache');
    header('Expires: 0');
    echo 'Unauthorized';
    exit;
}

header('Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

$dataFile = __DIR__ . '/tasks.json';
$data = json_decode(file_get_contents($dataFile), true);
$tasks = $data['tasks'] ?? [];
$income = $data['income'] ?? ['enabled' => true, 'monthlyTarget' => 10000, 'entries' => []];

$categories = [
    'schedule'    => ['label' => '📅 Schedule 💪',  'icon' => '📅'],
    'real-estate' => ['label' => '🏠 Real Estate', 'icon' => '🏠'],
    'career'      => ['label' => '💼 Career',      'icon' => '💼'],
    'personal'    => ['label' => '🏠 Personal',    'icon' => '🏠'],
    'seo'         => ['label' => '🔍 SEO',         'icon' => '🔍'],
    'goals'       => ['label' => '🎯 Goals',       'icon' => '🎯'],
    'rosey'       => ['label' => '🤖 Rosey',       'icon' => '🤖']
];

$columns = [
    'new'         => ['label' => 'New',         'color' => '#0a84ff'],
    'in-progress' => ['label' => 'In Progress', 'color' => '#ff9f0a'],
    'stuck'       => ['label' => 'Stuck',       'color' => '#ff453a'],
    'completed'   => ['label' => 'Completed',   'color' => '#30d158']
];

$priorityColors = [
    'high'   => '#ff453a',
    'medium' => '#ff9f0a',
    'low'    => '#30d158'
];

// Migrate old "pending" status to "new"
$needsSave = false;
foreach ($tasks as &$task) {
    if (($task['status'] ?? '') === 'pending') {
        $task['status'] = 'new';
        $needsSave = true;
    }
}
unset($task);
if ($needsSave) {
    $data['tasks'] = $tasks;
    file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT));
}

$grouped = [];
foreach ($categories as $cat => $cfg) {
    $grouped[$cat] = array_fill_keys(array_keys($columns), []);
}
foreach ($tasks as $task) {
    $cat = $task['category'] ?? 'personal';
    $status = $task['status'] ?? 'new';
    if (!isset($grouped[$cat])) $cat = 'personal';
    if (!isset($grouped[$cat][$status])) $status = 'new';
    $grouped[$cat][$status][] = $task;
}

foreach ($grouped as $cat => $statuses) {
    foreach ($statuses as $status => $list) {
        usort($list, function($a, $b) {
            return ($a['order'] ?? 0) <=> ($b['order'] ?? 0);
        });
        $grouped[$cat][$status] = $list;
    }
}

$outstanding = 0;
foreach ($tasks as $t) {
    if (($t['status'] ?? '') !== 'completed') $outstanding++;
}

// Income calculations
$incomeEntries = $income['entries'] ?? [];
$monthlyTarget = $income['monthlyTarget'] ?? 10000;
$currentMonth = date('Y-m');
$currentMonthTotal = 0;
$lastMonth = date('Y-m', strtotime('-1 month'));
$lastMonthTotal = 0;
foreach ($incomeEntries as $entry) {
    $entryMonth = substr($entry['date'], 0, 7);
    if ($entryMonth === $currentMonth) $currentMonthTotal += floatval($entry['amount']);
    if ($entryMonth === $lastMonth) $lastMonthTotal += floatval($entry['amount']);
}
$progressPct = $monthlyTarget > 0 ? min(100, round(($currentMonthTotal / $monthlyTarget) * 100, 1)) : 0;
$monthOverMonth = $lastMonthTotal > 0 ? round((($currentMonthTotal - $lastMonthTotal) / $lastMonthTotal) * 100, 1) : 0;

// Goal sub-categories
$goalHealth = [];
$goalFamily = [];
$goalIncome = [];
foreach (array_merge($grouped['goals']['new'], $grouped['goals']['in-progress'], $grouped['goals']['completed'], $grouped['goals']['stuck']) as $task) {
    if (stripos($task['title'], 'health') !== false || stripos($task['title'], 'wake') !== false || stripos($task['title'], 'exercise') !== false || stripos($task['title'], 'wind down') !== false || stripos($task['title'], 'sleep') !== false) {
        $goalHealth[] = $task;
    } elseif (stripos($task['title'], 'family') !== false) {
        $goalFamily[] = $task;
    } else {
        $goalIncome[] = $task;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Mission Board</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 16px;
            line-height: 1.5;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }
        h1 { font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }
        .btn {
            background: #ff9f0a;
            color: #000;
            border: none;
            padding: 10px 16px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
        }

        /* Mission Banner */
        .mission-banner {
            background: linear-gradient(135deg, #1c1c1c 0%, #141414 100%);
            border: 1px solid #2c2c2c;
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
        }
        .mission-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #ff9f0a, #ff453a, #30d158, #0a84ff);
        }
        .mission-label {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #ff9f0a;
            margin-bottom: 8px;
        }
        .mission-text {
            font-size: 16px;
            font-weight: 600;
            line-height: 1.6;
            color: #f5f5f5;
        }
        .mission-why {
            margin-top: 10px;
            font-size: 13px;
            color: #888;
            line-height: 1.5;
            font-style: italic;
        }
        .mission-why strong {
            color: #e0e0e0;
            font-style: normal;
        }

        .tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            overflow-x: auto;
            padding-bottom: 4px;
        }
        .tab {
            background: #1c1c1c;
            border: 1px solid #2c2c2c;
            color: #e0e0e0;
            padding: 10px 14px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .tab.active {
            background: #ff9f0a;
            color: #000;
            border-color: #ff9f0a;
        }
        .badge {
            background: transparent;
            color: #888;
            font-size: 11px;
            font-weight: 700;
            padding: 0 4px;
            border-radius: 0;
            min-width: auto;
            text-align: center;
        }
        .tab.active .badge { background: transparent; color: #000; }
        .outstanding {
            margin-bottom: 16px;
            font-size: 14px;
            font-weight: 600;
            color: #ff453a;
        }
        .board {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        @media (min-width: 1000px) {
            .board { grid-template-columns: repeat(4, 1fr); }
        }
        .column {
            background: #141414;
            border-radius: 16px;
            padding: 12px;
            border: 1px solid #1f1f1f;
            min-height: 200px;
            display: flex;
            flex-direction: column;
        }
        .column-title {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            padding-left: 4px;
            color: #888;
        }
        .task-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            min-height: 120px;
            flex: 1;
        }
        .task {
            background: #1c1c1c;
            border-radius: 12px;
            padding: 12px;
            border-left: 4px solid #666;
            cursor: grab;
            position: relative;
            transition: transform 0.1s, box-shadow 0.1s;
        }
        .task.dragging { opacity: 0.5; transform: scale(0.98); }
        .task-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
            padding-right: 28px;
        }
        .task-meta {
            display: flex;
            gap: 6px;
            align-items: center;
            flex-wrap: wrap;
        }
        .priority {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 2px 6px;
            border-radius: 4px;
            background: #333;
            color: #fff;
        }
        .task-notes {
            font-size: 12px;
            color: #888;
            margin-top: 6px;
            line-height: 1.4;
        }
        .edit-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            background: transparent;
            border: none;
            color: #888;
            cursor: pointer;
            font-size: 16px;
            padding: 4px;
        }
        .edit-btn:hover { color: #fff; }
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.85);
            z-index: 100;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        .modal-overlay.open { display: flex; }
        .modal {
            background: #1c1c1c;
            border-radius: 16px;
            padding: 20px;
            width: 100%;
            max-width: 420px;
            border: 1px solid #2c2c2c;
        }
        .modal h2 { margin-bottom: 16px; font-size: 18px; }
        .form-row { margin-bottom: 12px; }
        label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #888;
            margin-bottom: 4px;
            text-transform: uppercase;
        }
        input, textarea, select {
            width: 100%;
            background: #0a0a0a;
            border: 1px solid #2c2c2c;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
        }
        textarea { min-height: 80px; resize: vertical; }
        .modal-actions {
            display: flex;
            gap: 10px;
            margin-top: 16px;
        }
        .modal-actions .btn { flex: 1; }
        .btn-secondary {
            background: #333;
            color: #e0e0e0;
        }
        .btn-danger {
            background: #ff453a;
            color: #fff;
        }
        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #30d158;
            color: #000;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
            display: none;
            z-index: 200;
        }
        .toast.error { background: #ff453a; color: #fff; }

        /* Goals tab */
        .goals-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .income-panel {
            background: #141414;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid #1f1f1f;
        }
        .income-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .income-title {
            font-size: 16px;
            font-weight: 700;
            color: #ff9f0a;
        }
        .income-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }
        @media (min-width: 600px) {
            .income-stats { grid-template-columns: repeat(4, 1fr); }
        }
        .stat-box {
            background: #1c1c1c;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            color: #fff;
        }
        .stat-label {
            font-size: 11px;
            color: #888;
            margin-top: 4px;
            text-transform: uppercase;
        }
        .progress-bar {
            background: #1c1c1c;
            border-radius: 8px;
            height: 24px;
            overflow: hidden;
            margin-bottom: 16px;
        }
        .progress-fill {
            background: linear-gradient(90deg, #30d158, #ff9f0a);
            height: 100%;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            font-size: 12px;
            font-weight: 700;
            color: #000;
            transition: width 0.5s;
        }
        .income-form {
            display: grid;
            grid-template-columns: 1fr 1fr 2fr auto;
            gap: 10px;
            align-items: end;
        }
        @media (max-width: 600px) {
            .income-form { grid-template-columns: 1fr; }
        }
        .income-table {
            width: 100%;
            margin-top: 16px;
            border-collapse: collapse;
        }
        .income-table th,
        .income-table td {
            text-align: left;
            padding: 10px;
            font-size: 13px;
            border-bottom: 1px solid #1f1f1f;
        }
        .income-table th {
            color: #888;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
        }
        .income-table td { color: #e0e0e0; }
        .income-delete {
            background: transparent;
            border: none;
            color: #ff453a;
            cursor: pointer;
            font-size: 16px;
        }
        .goals-board {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
        }
        @media (min-width: 768px) {
            .goals-board { grid-template-columns: repeat(3, 1fr); }
        }
        .goal-category {
            background: #141414;
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #1f1f1f;
        }
        .goal-cat-title {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .goal-health { color: #30d158; }
        .goal-family { color: #64d2ff; }
        .goal-income { color: #ff9f0a; }
        .goal-list {
            list-style: none;
        }
        .goal-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #1f1f1f;
            font-size: 14px;
        }
        .goal-item:last-child { border-bottom: none; }
        .goal-checkbox {
            width: 18px;
            height: 18px;
            border-radius: 5px;
            border: 2px solid #444;
            flex-shrink: 0;
            margin-top: 2px;
            cursor: pointer;
            appearance: none;
            -webkit-appearance: none;
        }
        .goal-checkbox:checked {
            background: #30d158;
            border-color: #30d158;
        }
        .goal-checkbox:checked::after {
            content: '\2713';
            display: block;
            color: #000;
            font-size: 12px;
            font-weight: 700;
            text-align: center;
            line-height: 14px;
        }
        .goal-delete {
            background: transparent;
            border: none;
            color: #ff453a;
            cursor: pointer;
            font-size: 14px;
            margin-left: auto;
        }
        .add-goal-btn {
            background: #1c1c1c;
            border: 1px dashed #444;
            color: #888;
            padding: 10px;
            border-radius: 8px;
            width: 100%;
            margin-top: 10px;
            cursor: pointer;
            font-size: 13px;
        }
        .add-goal-btn:hover {
            border-color: #ff9f0a;
            color: #ff9f0a;
        }

        /* Schedule tab grid */
        .sched-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }
        @media (min-width: 1000px) {
            .sched-grid { grid-template-columns: repeat(3, 1fr); }
        }
        .sched-day {
            background: #141414;
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #1f1f1f;
        }
        .sched-day-title {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .sched-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .sched-table td {
            padding: 5px 0;
            border-bottom: 1px solid #1f1f1f;
        }
        .sched-table tr:last-child td { border-bottom: none; }
        .sched-overview {
            background: #141414;
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #1f1f1f;
        }
    /* Schedule tab override */
        #board-schedule {
            display: block;
            grid-template-columns: 1fr !important;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Mission Board</h1>
        <button class="btn" onclick="openModal()">+ New Task</button>
    </div>

    <!-- Mission Banner -->
    <div class="mission-banner">
        <div class="mission-label">Mission</div>
        <div class="mission-text">
            Build generational wealth through real estate. Create total time freedom — control my schedule, travel when I want, and spend every moment with the people who matter most.
        </div>
        <div class="mission-why">
            <strong>My Why:</strong> My family. I want to control my time. Spend it how I want, where I want, when I want, and with who I want. Travel. Freedom. No regrets.
        </div>
    </div>

    <div class="tabs" id="tabs">
        <?php foreach ($categories as $cat => $cfg):
            $catOutstanding = 0;
            foreach ($grouped[$cat] as $status => $list) {
                if ($status !== 'completed') $catOutstanding += count($list);
            }
        ?>
            <button class="tab <?php echo $cat === 'schedule' ? 'active' : ''; ?>" data-cat="<?php echo $cat; ?>" onclick="switchTab('<?php echo $cat; ?>')">
                <?php echo $cfg['label']; ?>
                <?php if ($cat !== 'schedule'): ?><span class="badge"><?php echo $catOutstanding; ?></span><?php endif; ?>
            </button>
        <?php endforeach; ?>
    </div>

    <div class="outstanding">🚨 Outstanding Tasks: <?php echo $outstanding; ?></div>

    <!-- Schedule Panel -->
    <div class="board" id="board-schedule" style="display:block;">
        <div class="sched-grid">
            <div class="sched-day">
                <div class="sched-day-title" style="color:#64d2ff;">📅 MONDAY — 5:15 AM Wake</div>
                <table class="sched-table">
                    <tr><td style="width:60px;color:#888;">5:15</td><td style="color:#f0f0f0;font-weight:600;">Wake → Gym (legs/core)</td></tr>
                    <tr><td style="color:#888;">6:45</td><td style="color:#ccc;">Shower, dress</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Family breakfast</td></tr>
                    <tr><td style="color:#888;">9:00</td><td style="color:#ccc;">W-2 Block 1</td></tr>
                    <tr><td style="color:#888;">12:00</td><td style="color:#f0f0f0;font-weight:600;">Family lunch</td></tr>
                    <tr><td style="color:#888;">1:15</td><td style="color:#ccc;">W-2 Block 2 + 6 PM meeting</td></tr>
                    <tr><td style="color:#888;">6:00</td><td style="color:#f0f0f0;font-weight:600;">Dinner + family</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Kids bedtime</td></tr>
                    <tr><td style="color:#888;">8:00</td><td style="color:#f0f0f0;font-weight:600;">Wife time</td></tr>
                    <tr><td style="color:#888;">9:30</td><td style="color:#ccc;">Bed</td></tr>
                </table>
            </div>
            <div class="sched-day">
                <div class="sched-day-title" style="color:#ff9f0a;">🔥 TUESDAY — 5:15 AM Wake</div>
                <table class="sched-table">
                    <tr><td style="width:60px;color:#888;">5:15</td><td style="color:#f0f0f0;font-weight:600;">Wake → Business Window</td></tr>
                    <tr><td style="color:#888;">6:45</td><td style="color:#ccc;">Shower, dress</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Family breakfast</td></tr>
                    <tr><td style="color:#888;">9:00</td><td style="color:#ccc;">W-2 Block 1</td></tr>
                    <tr><td style="color:#888;">12:00</td><td style="color:#f0f0f0;font-weight:600;">Family lunch</td></tr>
                    <tr><td style="color:#888;">1:15</td><td style="color:#ccc;">W-2 Block 2</td></tr>
                    <tr><td style="color:#888;">5:00</td><td style="color:#f0f0f0;font-weight:600;">Dinner + family</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Kids bedtime</td></tr>
                    <tr><td style="color:#888;">8:00</td><td style="color:#f0f0f0;font-weight:600;">Wife time</td></tr>
                    <tr><td style="color:#888;">9:30</td><td style="color:#ccc;">Bed</td></tr>
                </table>
            </div>
            <div class="sched-day">
                <div class="sched-day-title" style="color:#ff9f0a;">🔥 WEDNESDAY — 5:15 AM Wake</div>
                <table class="sched-table">
                    <tr><td style="width:60px;color:#888;">5:15</td><td style="color:#f0f0f0;font-weight:600;">Wake → Business Window</td></tr>
                    <tr><td style="color:#888;">6:45</td><td style="color:#ccc;">Shower, dress</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Family breakfast</td></tr>
                    <tr><td style="color:#888;">9:00</td><td style="color:#ccc;">W-2 Block 1</td></tr>
                    <tr><td style="color:#888;">12:00</td><td style="color:#f0f0f0;font-weight:600;">Family lunch</td></tr>
                    <tr><td style="color:#888;">1:15</td><td style="color:#ccc;">W-2 Block 2</td></tr>
                    <tr><td style="color:#888;">5:00</td><td style="color:#f0f0f0;font-weight:600;">Dinner + family</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Kids bedtime</td></tr>
                    <tr><td style="color:#888;">8:00</td><td style="color:#f0f0f0;font-weight:600;">Wife time</td></tr>
                    <tr><td style="color:#888;">9:30</td><td style="color:#ccc;">Bed</td></tr>
                </table>
            </div>
            <div class="sched-day">
                <div class="sched-day-title" style="color:#ff453a;">🚨 THURSDAY — 5:15 AM Wake (Late Day)</div>
                <table class="sched-table">
                    <tr><td style="width:60px;color:#888;">5:15</td><td style="color:#f0f0f0;font-weight:600;">Wake → Morning prep</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Family breakfast</td></tr>
                    <tr><td style="color:#888;">9:00</td><td style="color:#ccc;">W-2 Block 1</td></tr>
                    <tr><td style="color:#888;">12:00</td><td style="color:#f0f0f0;font-weight:600;">Family lunch</td></tr>
                    <tr><td style="color:#888;">1:15</td><td style="color:#ccc;">W-2 Block 2 + 6 PM meeting</td></tr>
                    <tr><td style="color:#888;">6:00</td><td style="color:#f0f0f0;font-weight:600;">Dinner + family</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Kids bedtime</td></tr>
                    <tr><td style="color:#888;">8:00</td><td style="color:#f0f0f0;font-weight:600;">GYM — evening session</td></tr>
                    <tr><td style="color:#888;">9:30</td><td style="color:#f0f0f0;font-weight:600;">Business Power Block</td></tr>
                    <tr><td style="color:#888;">11:30</td><td style="color:#ccc;">Bed</td></tr>
                </table>
            </div>
            <div class="sched-day">
                <div class="sched-day-title" style="color:#30d158;">😴 FRIDAY — 6:30 AM Wake (Sleep In)</div>
                <table class="sched-table">
                    <tr><td style="width:60px;color:#888;">6:30</td><td style="color:#f0f0f0;font-weight:600;">Wake → Sleep in</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Family breakfast</td></tr>
                    <tr><td style="color:#888;">9:00</td><td style="color:#ccc;">W-2 Block 1</td></tr>
                    <tr><td style="color:#888;">12:00</td><td style="color:#f0f0f0;font-weight:600;">Family lunch</td></tr>
                    <tr><td style="color:#888;">1:15</td><td style="color:#ccc;">W-2 Block 2</td></tr>
                    <tr><td style="color:#888;">5:00</td><td style="color:#f0f0f0;font-weight:600;">Dinner + family</td></tr>
                    <tr><td style="color:#888;">7:00</td><td style="color:#f0f0f0;font-weight:600;">Kids bedtime</td></tr>
                    <tr><td style="color:#888;">8:00</td><td style="color:#f0f0f0;font-weight:600;">Wife time</td></tr>
                    <tr><td style="color:#888;">9:30</td><td style="color:#f0f0f0;font-weight:600;">Business Power Block</td></tr>
                    <tr><td style="color:#888;">11:30</td><td style="color:#ccc;">Bed</td></tr>
                </table>
            </div>
            <div class="sched-overview">
                <div style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#ff9f0a;margin-bottom:12px;">Weekly Overview</div>
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <tr><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#888;">Business</td><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#f0f0f0;font-weight:600;">Tue/Wed 5:30–6:45 AM + Thu/Fri 9:30–11:30 PM (6.5h)</td></tr>
                    <tr><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#888;">Gym</td><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#f0f0f0;font-weight:600;">Mon 5:30 AM + Thu 8:00 PM (3h)</td></tr>
                    <tr><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#888;">W-2</td><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#ccc;">43 hours</td></tr>
                    <tr><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#888;">Family</td><td style="padding:6px 8px;border-bottom:1px solid #1f1f1f;color:#ccc;">28.75 hours</td></tr>
                    <tr><td style="padding:6px 8px;color:#888;">Reddit</td><td style="padding:6px 8px;color:#ccc;">After 9 PM (Mon–Wed/Fri) — 30 min max</td></tr>
                </table>
            </div>
        </div>

        <!-- Income Tracker (Schedule tab) -->
        <div class="income-panel">
            <div class="income-header">
                <div class="income-title">💰 Income Tracker</div>
                <button class="btn" style="padding: 6px 12px; font-size: 12px;" onclick="document.getElementById('income-form-row-schedule').style.display='grid'">+ Add Income</button>
            </div>
            <div class="income-stats">
                <div class="stat-box">
                    <div class="stat-value">$<?php echo number_format($currentMonthTotal); ?></div>
                    <div class="stat-label">This Month</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">$<?php echo number_format($monthlyTarget); ?></div>
                    <div class="stat-label">Target</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value"><?php echo $progressPct; ?>%</div>
                    <div class="stat-label">Progress</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: <?php echo $monthOverMonth >= 0 ? '#30d158' : '#ff453a'; ?>">
                        <?php echo ($monthOverMonth >= 0 ? '+' : '') . $monthOverMonth; ?>%
                    </div>
                    <div class="stat-label">vs Last Month</div>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: <?php echo $progressPct; ?>%"><?php echo $progressPct; ?>%</div>
            </div>
            <div class="income-form" id="income-form-row-schedule" style="display:none;">
                <div>
                    <label>Date</label>
                    <input type="date" id="income-date-schedule" value="<?php echo date('Y-m-d'); ?>">
                </div>
                <div>
                    <label>Amount ($)</label>
                    <input type="number" id="income-amount-schedule" placeholder="0.00" step="0.01">
                </div>
                <div>
                    <label>Source / Notes</label>
                    <input type="text" id="income-source-schedule" placeholder="e.g. Commission, wholesale deal...">
                </div>
                <div>
                    <button class="btn" onclick="addIncomeSchedule()">Add</button>
                </div>
            </div>
            <?php if (!empty($incomeEntries)): ?>
            <table class="income-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Source</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_reverse($incomeEntries) as $entry): ?>
                    <tr data-date="<?php echo htmlspecialchars($entry['date']); ?>" data-amount="<?php echo floatval($entry['amount']); ?>">
                        <td><?php echo htmlspecialchars($entry['date']); ?></td>
                        <td>$<?php echo number_format(floatval($entry['amount']), 2); ?></td>
                        <td><?php echo htmlspecialchars($entry['source'] ?? ''); ?></td>
                        <td><button class="income-delete" onclick="deleteIncome('<?php echo htmlspecialchars($entry['date']); ?>', <?php echo floatval($entry['amount']); ?>)">×</button></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
            <?php endif; ?>
        </div>

        <!-- Goals (Schedule tab) -->
        <div class="goals-board">
            <div class="goal-category">
                <div class="goal-cat-title goal-health">💪 Health</div>
                <ul class="goal-list">
                    <?php foreach ($goalHealth as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('health')">+ Add Health Goal</button>
            </div>
            <div class="goal-category">
                <div class="goal-cat-title goal-family">👨‍👩‍👧 Family</div>
                <ul class="goal-list">
                    <?php foreach ($goalFamily as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('family')">+ Add Family Goal</button>
            </div>
            <div class="goal-category">
                <div class="goal-cat-title goal-income">💰 Income</div>
                <ul class="goal-list">
                    <?php foreach ($goalIncome as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('income')">+ Add Income Goal</button>
            </div>
        </div>
    </div>

    <?php foreach ($categories as $cat => $cfg): ?>
    <?php if ($cat === 'schedule'): continue; endif; ?>
    <?php if ($cat === 'goals'): ?>
    <div class="board goals-container" id="board-<?php echo $cat; ?>" style="display:none;">
        <!-- Income Tracking Panel -->
        <div class="income-panel">
            <div class="income-header">
                <div class="income-title">💰 Income Tracker</div>
                <button class="btn" style="padding: 6px 12px; font-size: 12px;" onclick="document.getElementById('income-form-row').style.display='grid'">+ Add Income</button>
            </div>
            <div class="income-stats">
                <div class="stat-box">
                    <div class="stat-value">$<?php echo number_format($currentMonthTotal); ?></div>
                    <div class="stat-label">This Month</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">$<?php echo number_format($monthlyTarget); ?></div>
                    <div class="stat-label">Target</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value"><?php echo $progressPct; ?>%</div>
                    <div class="stat-label">Progress</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: <?php echo $monthOverMonth >= 0 ? '#30d158' : '#ff453a'; ?>">
                        <?php echo ($monthOverMonth >= 0 ? '+' : '') . $monthOverMonth; ?>%
                    </div>
                    <div class="stat-label">vs Last Month</div>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: <?php echo $progressPct; ?>%"><?php echo $progressPct; ?>%</div>
            </div>
            <div class="income-form" id="income-form-row" style="display:none;">
                <div>
                    <label>Date</label>
                    <input type="date" id="income-date" value="<?php echo date('Y-m-d'); ?>">
                </div>
                <div>
                    <label>Amount ($)</label>
                    <input type="number" id="income-amount" placeholder="0.00" step="0.01">
                </div>
                <div>
                    <label>Source / Notes</label>
                    <input type="text" id="income-source" placeholder="e.g. Commission, wholesale deal...">
                </div>
                <div>
                    <button class="btn" onclick="addIncome()">Add</button>
                </div>
            </div>
            <?php if (!empty($incomeEntries)): ?>
            <table class="income-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Source</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_reverse($incomeEntries) as $entry): ?>
                    <tr data-date="<?php echo htmlspecialchars($entry['date']); ?>" data-amount="<?php echo floatval($entry['amount']); ?>">
                        <td><?php echo htmlspecialchars($entry['date']); ?></td>
                        <td>$<?php echo number_format(floatval($entry['amount']), 2); ?></td>
                        <td><?php echo htmlspecialchars($entry['source'] ?? ''); ?></td>
                        <td><button class="income-delete" onclick="deleteIncome('<?php echo htmlspecialchars($entry['date']); ?>', <?php echo floatval($entry['amount']); ?>)">×</button></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
            <?php endif; ?>
        </div>

        <!-- Goals Categories -->
        <div class="goals-board">
            <div class="goal-category">
                <div class="goal-cat-title goal-health">💪 Health</div>
                <ul class="goal-list" id="goals-health">
                    <?php foreach ($goalHealth as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('health')">+ Add Health Goal</button>
            </div>
            <div class="goal-category">
                <div class="goal-cat-title goal-family">👨‍👩‍👧 Family</div>
                <ul class="goal-list" id="goals-family">
                    <?php foreach ($goalFamily as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('family')">+ Add Family Goal</button>
            </div>
            <div class="goal-category">
                <div class="goal-cat-title goal-income">💰 Income</div>
                <ul class="goal-list" id="goals-income">
                    <?php foreach ($goalIncome as $task): ?>
                    <li class="goal-item" data-id="<?php echo htmlspecialchars($task['id']); ?>">
                        <input type="checkbox" class="goal-checkbox" <?php echo ($task['status'] ?? '') === 'completed' ? 'checked' : ''; ?> onchange="toggleGoal('<?php echo htmlspecialchars($task['id']); ?>')">
                        <div style="flex:1;">
                            <div style="font-weight:600;"><?php echo htmlspecialchars($task['title']); ?></div>
                            <?php if (!empty($task['notes'])): ?>
                            <div style="font-size: 12px; color: #888; margin-top: 2px;"><?php echo htmlspecialchars($task['notes']); ?></div>
                            <?php endif; ?>
                        </div>
                        <button class="goal-delete" onclick="deleteGoalTask('<?php echo htmlspecialchars($task['id']); ?>')">×</button>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <button class="add-goal-btn" onclick="openGoalModal('income')">+ Add Income Goal</button>
            </div>
        </div>
    </div>
    <?php else: ?>
    <div class="board" id="board-<?php echo $cat; ?>" style="display:none;">
        <?php foreach ($columns as $status => $colCfg): ?>
        <div class="column">
            <div class="column-title" style="color:<?php echo $colCfg['color']; ?>"><?php echo $colCfg['label']; ?></div>
            <div class="task-list"
                 data-cat="<?php echo $cat; ?>"
                 data-status="<?php echo $status; ?>"
                 ondragover="allowDrop(event)"
                 ondrop="drop(event)">
                <?php foreach ($grouped[$cat][$status] as $task):
                    $priColor = $priorityColors[$task['priority'] ?? 'medium'] ?? '#ff9f0a';
                ?>
                <div class="task"
                     draggable="true"
                     ondragstart="drag(event)"
                     ondblclick="editTask('<?php echo htmlspecialchars($task['id']); ?>')"
                     data-id="<?php echo htmlspecialchars($task['id']); ?>"
                     style="border-left-color:<?php echo $priColor; ?>">
                    <button class="edit-btn" onclick="event.stopPropagation(); editTask('<?php echo htmlspecialchars($task['id']); ?>')">✎</button>
                    <div class="task-title"><?php echo htmlspecialchars($task['title']); ?></div>
                    <div class="task-meta">
                        <span class="priority" style="background:<?php echo $priColor; ?>"><?php echo $task['priority'] ?? 'medium'; ?></span>
                    </div>
                    <?php if (!empty($task['notes'])): ?>
                    <div class="task-notes"><?php echo nl2br(htmlspecialchars($task['notes'])); ?></div>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
    <?php endif; ?>
    <?php endforeach; ?>

    <div class="modal-overlay" id="modal">
        <div class="modal">
            <h2 id="modal-title">New Task</h2>
            <input type="hidden" id="task-id">
            <div class="form-row">
                <label>Title</label>
                <input type="text" id="task-title" placeholder="Task title">
            </div>
            <div class="form-row">
                <label>Category</label>
                <select id="task-category">
                    <?php foreach ($categories as $cat => $cfg): ?>
                    <option value="<?php echo $cat; ?>"><?php echo $cfg['label']; ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="form-row">
                <label>Status</label>
                <select id="task-status">
                    <?php foreach ($columns as $status => $colCfg): ?>
                    <option value="<?php echo $status; ?>"><?php echo $colCfg['label']; ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="form-row">
                <label>Priority</label>
                <select id="task-priority">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
            <div class="form-row">
                <label>Notes</label>
                <textarea id="task-notes" placeholder="Context..."></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn btn-danger" id="delete-btn" style="display:none" onclick="deleteTask()">Delete</button>
                <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button class="btn" onclick="saveTask()">Save</button>
            </div>
        </div>
    </div>

    <!-- Goal Modal -->
    <div class="modal-overlay" id="goal-modal">
        <div class="modal">
            <h2>Add Goal</h2>
            <input type="hidden" id="goal-category-input">
            <div class="form-row">
                <label>Goal Title</label>
                <input type="text" id="goal-title-input" placeholder="e.g. Read 10 pages daily">
            </div>
            <div class="form-row">
                <label>Notes</label>
                <textarea id="goal-notes-input" placeholder="Why this matters..."></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn" onclick="saveGoal()">Add Goal</button>
                <button class="btn btn-secondary" onclick="closeGoalModal()">Cancel</button>
            </div>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        const tasks = <?php echo json_encode($tasks); ?>;
        let draggedId = null;

        function switchTab(cat) {
            document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.cat === cat));
            document.querySelectorAll('.board').forEach(b => b.style.display = b.id === 'board-' + cat ? '' : 'none');
        }

        function drag(ev) {
            draggedId = ev.target.dataset.id;
            ev.target.classList.add('dragging');
            ev.dataTransfer.effectAllowed = 'move';
        }

        document.addEventListener('dragend', function(e) {
            if (e.target.classList.contains('task')) e.target.classList.remove('dragging');
        });

        function allowDrop(ev) {
            ev.preventDefault();
        }

        function drop(ev) {
            ev.preventDefault();
            let list = ev.target.closest('.task-list');
            if (!list) {
                const col = ev.target.closest('.column');
                if (col) list = col.querySelector('.task-list');
            }
            if (!list || !draggedId) return;

            const newCat = list.dataset.cat;
            const newStatus = list.dataset.status;
            const afterElement = getDragAfterElement(list, ev.clientY);

            if (afterElement) {
                list.insertBefore(document.querySelector(`[data-id="${draggedId}"]`), afterElement);
            } else {
                list.appendChild(document.querySelector(`[data-id="${draggedId}"]`));
            }

            updateOrder(list, newCat, newStatus);
        }

        function getDragAfterElement(container, y) {
            const draggableElements = [...container.querySelectorAll('.task:not(.dragging)')];
            return draggableElements.reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;
                if (offset < 0 && offset > closest.offset) {
                    return { offset: offset, element: child };
                }
                return closest;
            }, { offset: Number.NEGATIVE_INFINITY }).element;
        }

        function updateOrder(list, cat, status) {
            const ids = [...list.querySelectorAll('.task')].map(t => t.dataset.id);
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'reorder', category: cat, status: status, orderedIds: ids })
            })
            .then(r => r.json())
            .then(d => {
                if (!d.success) showToast(d.error || 'Save failed', true);
                else showToast('Updated');
            })
            .catch(e => showToast('Network error', true));
        }

        function openModal(id = null) {
            const modal = document.getElementById('modal');
            document.getElementById('modal-title').textContent = id ? 'Edit Task' : 'New Task';
            document.getElementById('delete-btn').style.display = id ? 'block' : 'none';
            if (id) {
                const t = tasks.find(x => x.id === id);
                document.getElementById('task-id').value = t.id;
                document.getElementById('task-title').value = t.title;
                document.getElementById('task-category').value = t.category;
                document.getElementById('task-status').value = t.status;
                document.getElementById('task-priority').value = t.priority;
                document.getElementById('task-notes').value = t.notes || '';
            } else {
                document.getElementById('task-id').value = '';
                document.getElementById('task-title').value = '';
                document.getElementById('task-category').value = 'real-estate';
                document.getElementById('task-status').value = 'new';
                document.getElementById('task-priority').value = 'medium';
                document.getElementById('task-notes').value = '';
            }
            modal.classList.add('open');
        }

        function closeModal() {
            document.getElementById('modal').classList.remove('open');
        }

        function editTask(id) {
            openModal(id);
        }

        function saveTask() {
            const id = document.getElementById('task-id').value;
            const task = {
                id: id || undefined,
                title: document.getElementById('task-title').value.trim(),
                category: document.getElementById('task-category').value,
                status: document.getElementById('task-status').value,
                priority: document.getElementById('task-priority').value,
                notes: document.getElementById('task-notes').value.trim()
            };
            if (!task.title) { showToast('Title required', true); return; }

            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'save', task: task })
            })
            .then(r => r.json())
            .then(d => {
                if (d.success) { closeModal(); location.reload(); }
                else showToast(d.error || 'Save failed', true);
            })
            .catch(e => showToast('Network error', true));
        }

        function deleteTask() {
            const id = document.getElementById('task-id').value;
            if (!confirm('Delete this task?')) return;
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'delete', id: id })
            })
            .then(r => r.json())
            .then(d => {
                if (d.success) { closeModal(); location.reload(); }
                else showToast(d.error || 'Delete failed', true);
            })
            .catch(e => showToast('Network error', true));
        }

        function openGoalModal(subcat) {
            document.getElementById('goal-category-input').value = subcat;
            document.getElementById('goal-title-input').value = '';
            document.getElementById('goal-notes-input').value = '';
            document.getElementById('goal-modal').classList.add('open');
        }
        function closeGoalModal() { document.getElementById('goal-modal').classList.remove('open'); }
        function saveGoal() {
            const subcat = document.getElementById('goal-category-input').value;
            const title = document.getElementById('goal-title-input').value.trim();
            const notes = document.getElementById('goal-notes-input').value.trim();
            if (!title) { showToast('Title required', true); return; }
            const prefix = subcat === 'health' ? 'gh' : subcat === 'family' ? 'gf' : 'gi';
            const emoji = subcat === 'health' ? '💪' : subcat === 'family' ? '👨‍👩‍👧' : '💰';
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'save', task: {
                    title: emoji + ' ' + title.charAt(0).toUpperCase() + title.slice(1),
                    category: 'goals',
                    status: 'new',
                    priority: 'medium',
                    notes: notes
                } })
            })
            .then(r => r.json())
            .then(d => { if (d.success) { closeGoalModal(); location.reload(); } else showToast(d.error || 'Save failed', true); })
            .catch(e => showToast('Network error', true));
        }
        function toggleGoal(id) {
            const task = tasks.find(x => x.id === id);
            const newStatus = task.status === 'completed' ? 'new' : 'completed';
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'save', task: { id: id, status: newStatus } })
            })
            .then(r => r.json())
            .then(d => { if (!d.success) showToast(d.error || 'Update failed', true); })
            .catch(e => showToast('Network error', true));
        }
        function deleteGoalTask(id) {
            if (!confirm('Delete this goal?')) return;
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'delete', id: id })
            })
            .then(r => r.json())
            .then(d => { if (d.success) { location.reload(); } else showToast(d.error || 'Delete failed', true); })
            .catch(e => showToast('Network error', true));
        }

        function addIncome() {
            const date = document.getElementById('income-date').value;
            const amount = parseFloat(document.getElementById('income-amount').value);
            const source = document.getElementById('income-source').value.trim();
            if (!date || isNaN(amount) || amount <= 0) { showToast('Valid date and amount required', true); return; }
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'addIncome', entry: { date, amount, source } })
            })
            .then(r => r.json())
            .then(d => { if (d.success) { location.reload(); } else showToast(d.error || 'Failed', true); })
            .catch(e => showToast('Network error', true));
        }
        function addIncomeSchedule() {
            const date = document.getElementById('income-date-schedule').value;
            const amount = parseFloat(document.getElementById('income-amount-schedule').value);
            const source = document.getElementById('income-source-schedule').value.trim();
            if (!date || isNaN(amount) || amount <= 0) { showToast('Valid date and amount required', true); return; }
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'addIncome', entry: { date, amount, source } })
            })
            .then(r => r.json())
            .then(d => { if (d.success) { location.reload(); } else showToast(d.error || 'Failed', true); })
            .catch(e => showToast('Network error', true));
        }
        function deleteIncome(date, amount) {
            if (!confirm('Delete this income entry?')) return;
            fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'deleteIncome', date, amount })
            })
            .then(r => r.json())
            .then(d => { if (d.success) { location.reload(); } else showToast(d.error || 'Failed', true); })
            .catch(e => showToast('Network error', true));
        }

        function showToast(msg, isError = false) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.className = 'toast' + (isError ? ' error' : '');
            t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 2500);
        }

        document.getElementById('modal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });
        document.getElementById('goal-modal').addEventListener('click', function(e) {
            if (e.target === this) closeGoalModal();
        });
    </script>
</body>
</html>
