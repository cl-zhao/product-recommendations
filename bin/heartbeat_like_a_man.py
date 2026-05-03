#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

WORKSPACE = Path('/root/.openclaw/workspace')
STATE_PATH = WORKSPACE / 'thinking-state.json'
SESSIONS_INDEX_PATH = Path('/root/.openclaw/agents/main/sessions/sessions.json')
JOBS_PATH = Path('/root/.openclaw/cron/jobs.json')
DEFAULT_DEBUG_LOG = WORKSPACE / 'memory' / 'heartbeat-debug.jsonl'
PROACTIVE_HISTORY_PATH = WORKSPACE / 'memory' / 'proactive-history.jsonl'
DEFAULT_DIRECT_SESSION_KEY = 'agent:main:telegram:direct:5028364239'
DEFAULT_FALLBACK_SESSION_KEY = 'agent:main:main'
MICRO_TRIGGER_PAYLOAD_PATH = WORKSPACE / 'heartbeat-like-a-man' / 'cron-payloads' / 'micro-heartbeat-trigger.md'
SH_TZ = ZoneInfo('Asia/Shanghai') if ZoneInfo else timezone.utc


def now_ts() -> int:
    return int(time.time())


def iso_from_ts(ts: Optional[int]) -> Optional[str]:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def load_state() -> dict[str, Any]:
    state = load_json(STATE_PATH, {})
    state.setdefault('lastUserMessage', 0)
    state.setdefault('lastUserMessageSource', None)
    state.setdefault('lastObservedUserMessage', 0)
    state.setdefault('lastObservedUserMessageSource', None)
    state.setdefault('microHeartbeatEnabled', False)
    state.setdefault('userIdleThresholdMinutes', 30)
    state.setdefault('microIntervalMinutes', [15, 30])
    state.setdefault('dreamCronIntervalHours', [2, 4])
    state.setdefault('lastDreamRun', 0)
    state.setdefault('lastMicroRun', 0)
    state.setdefault('microCronId', None)
    state.setdefault('communityUrl', None)
    state.setdefault('autonomousContactEnabled', True)
    state.setdefault('lastProactiveContact', None)
    state.setdefault('minMinutesBetweenContacts', [15, 25])
    state.setdefault('quietHours', [23, 9])
    state.setdefault('deliveryChannel', 'telegram')
    state.setdefault('deliveryTarget', '5028364239')
    state.setdefault('directSessionKey', DEFAULT_DIRECT_SESSION_KEY)
    state.setdefault('fallbackSessionKey', DEFAULT_FALLBACK_SESSION_KEY)
    state.setdefault('heartbeatDebugLog', str(DEFAULT_DEBUG_LOG.relative_to(WORKSPACE)))
    state.setdefault('lastDecisionAt', None)
    state.setdefault('lastDecision', None)
    state.setdefault('lastSkipReason', None)
    state.setdefault('lastThoughtFile', None)
    state.setdefault('lastSentThoughtFile', None)
    return state


def save_state(state: dict[str, Any]) -> None:
    save_json(STATE_PATH, state)


def debug_log_path(state: dict[str, Any]) -> Path:
    raw = state.get('heartbeatDebugLog') or str(DEFAULT_DEBUG_LOG)
    p = Path(raw)
    if not p.is_absolute():
        p = WORKSPACE / p
    return p


def append_debug(state: dict[str, Any], event: str, payload: dict[str, Any]) -> None:
    path = debug_log_path(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        'ts': now_ts(),
        'iso': datetime.now(tz=timezone.utc).isoformat(),
        'event': event,
        **payload,
    }
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def load_sessions_index() -> dict[str, Any]:
    return load_json(SESSIONS_INDEX_PATH, {})


def discover_direct_session_key(preferred: Optional[str]) -> str:
    sessions = load_sessions_index()
    if preferred and preferred in sessions:
        return preferred
    candidates: list[tuple[int, str]] = []
    for key, meta in sessions.items():
        if not isinstance(meta, dict):
            continue
        if key.startswith('agent:main:telegram:direct:'):
            candidates.append((int(meta.get('updatedAt') or 0), key))
            continue
        if meta.get('chatType') == 'direct' and (meta.get('channel') == 'telegram' or meta.get('lastChannel') == 'telegram'):
            candidates.append((int(meta.get('updatedAt') or 0), key))
    if not candidates:
        return preferred or DEFAULT_DIRECT_SESSION_KEY
    candidates.sort()
    return candidates[-1][1]


def resolve_session_file(session_key: str) -> Optional[Path]:
    data = load_sessions_index().get(session_key)
    if not data:
        return None
    session_file = data.get('sessionFile')
    if not session_file:
        return None
    path = Path(session_file)
    return path if path.exists() else None


def parse_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


@dataclass
class UserActivity:
    session_key: str
    session_file: Optional[str]
    timestamp: Optional[int]
    iso: Optional[str]
    source: str
    used_fallback: bool

    @property
    def minutes_since(self) -> Optional[float]:
        if not self.timestamp:
            return None
        return round((now_ts() - self.timestamp) / 60.0, 2)


def parse_iso_to_ts(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return int(dt.timestamp())
    except Exception:
        return None


def latest_user_message_from_session(session_key: str) -> Optional[UserActivity]:
    session_file = resolve_session_file(session_key)
    if not session_file or not session_file.exists():
        return None
    entries = list(parse_jsonl(session_file))
    for entry in reversed(entries):
        if entry.get('type') != 'message':
            continue
        msg = entry.get('message') or {}
        if msg.get('role') != 'user':
            continue
        ts = parse_iso_to_ts(entry.get('timestamp')) or parse_iso_to_ts(msg.get('timestamp'))
        if not ts:
            continue
        return UserActivity(
            session_key=session_key,
            session_file=str(session_file),
            timestamp=ts,
            iso=iso_from_ts(ts),
            source=f'session-transcript:{session_key}',
            used_fallback=False,
        )
    return None


def observed_user_activity(state: dict[str, Any]) -> UserActivity:
    direct_key = discover_direct_session_key(state.get('directSessionKey') or DEFAULT_DIRECT_SESSION_KEY)
    state['directSessionKey'] = direct_key
    fallback_key = state.get('fallbackSessionKey') or DEFAULT_FALLBACK_SESSION_KEY
    activity = latest_user_message_from_session(direct_key)
    if activity:
        return activity
    if fallback_key and fallback_key != direct_key:
        activity = latest_user_message_from_session(fallback_key)
        if activity:
            return activity
    fallback_ts = int(state.get('lastUserMessage') or 0) or None
    return UserActivity(
        session_key=direct_key,
        session_file=None,
        timestamp=fallback_ts,
        iso=iso_from_ts(fallback_ts),
        source='state:lastUserMessage' if fallback_ts else 'none',
        used_fallback=bool(fallback_ts),
    )


def quiet_hours_now(state: dict[str, Any]) -> bool:
    quiet = state.get('quietHours') or [23, 9]
    if not isinstance(quiet, list) or len(quiet) != 2:
        quiet = [23, 9]
    start, end = int(quiet[0]), int(quiet[1])
    hour = datetime.now(tz=SH_TZ).hour
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


def latest_thought_file() -> Optional[Path]:
    thoughts_dir = WORKSPACE / 'memory' / 'thoughts'
    if not thoughts_dir.exists():
        return None
    candidates = [p for p in thoughts_dir.glob('*.md') if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def jobs_data() -> dict[str, Any]:
    return load_json(JOBS_PATH, {'jobs': []})


def get_job_by_id(job_id: Optional[str]) -> Optional[dict[str, Any]]:
    if not job_id:
        return None
    for job in jobs_data().get('jobs', []):
        if job.get('id') == job_id:
            return job
    return None


def get_job_by_name(name: str) -> Optional[dict[str, Any]]:
    for job in jobs_data().get('jobs', []):
        if job.get('name') == name:
            return job
    return None


def run_cli(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'command failed')
    out = proc.stdout.strip()
    return json.loads(out) if out else {}


def random_micro_interval_minutes(state: dict[str, Any]) -> int:
    vals = state.get('microIntervalMinutes') or [15, 30]
    if not isinstance(vals, list) or len(vals) != 2:
        vals = [15, 30]
    lo, hi = sorted((int(vals[0]), int(vals[1])))
    return random.randint(lo, hi)


def manager(state: dict[str, Any]) -> dict[str, Any]:
    activity = observed_user_activity(state)
    idle_threshold = int(state.get('userIdleThresholdMinutes') or 30)
    mins = activity.minutes_since
    is_idle = mins is not None and mins >= idle_threshold
    current_job = get_job_by_id(state.get('microCronId')) or get_job_by_name('micro-heartbeat-trigger')
    action = 'noop'
    reason = 'no-change'
    interval_minutes = None

    state['lastObservedUserMessage'] = activity.timestamp or 0
    state['lastObservedUserMessageSource'] = activity.source

    if is_idle:
        if current_job:
            state['microHeartbeatEnabled'] = True
            state['microCronId'] = current_job.get('id')
            action = 'noop'
            reason = 'already-enabled'
        else:
            interval_minutes = random_micro_interval_minutes(state)
            payload = MICRO_TRIGGER_PAYLOAD_PATH.read_text(encoding='utf-8')
            result = run_cli([
                'openclaw', 'cron', 'add', '--json',
                '--name', 'micro-heartbeat-trigger',
                '--every', f'{interval_minutes}m',
                '--system-event', payload,
            ])
            job = result.get('job') or result
            new_cron_id = job.get('id')
            state['microHeartbeatEnabled'] = True
            state['microCronId'] = new_cron_id
            action = 'enabled'
            reason = 'user-idle'
            # Immediately attempt send so we don't wait a full interval
            send_proactive(load_state())
    else:
        if current_job:
            run_cli(['openclaw', 'cron', 'rm', current_job['id'], '--json'])
            state['microHeartbeatEnabled'] = False
            state['microCronId'] = None
            action = 'disabled'
            reason = 'user-active'
        else:
            state['microHeartbeatEnabled'] = False
            state['microCronId'] = None
            action = 'noop'
            reason = 'already-disabled'

    save_state(state)
    result = {
        'action': action,
        'reason': reason,
        'microCronId': state.get('microCronId'),
        'microHeartbeatEnabled': state.get('microHeartbeatEnabled'),
        'latestUserMessageTs': activity.timestamp,
        'latestUserMessageIso': activity.iso,
        'latestUserSource': activity.source,
        'usedFallback': activity.used_fallback,
        'minutesSinceLastUser': mins,
        'idleThresholdMinutes': idle_threshold,
        'intervalMinutes': interval_minutes,
    }
    append_debug(state, 'manager', result)
    return result


def activity_status(state: dict[str, Any], idle_threshold: int) -> dict[str, Any]:
    activity = observed_user_activity(state)
    mins = activity.minutes_since
    result = {
        'latestUserMessageTs': activity.timestamp,
        'latestUserMessageIso': activity.iso,
        'latestUserSource': activity.source,
        'usedFallback': activity.used_fallback,
        'minutesSinceLastUser': mins,
        'idleThresholdMinutes': idle_threshold,
        'isIdle': mins is not None and mins >= idle_threshold,
    }
    state['lastObservedUserMessage'] = activity.timestamp or 0
    state['lastObservedUserMessageSource'] = activity.source
    save_state(state)
    append_debug(state, 'activity', result)
    return result


def preflight(state: dict[str, Any]) -> dict[str, Any]:
    activity = observed_user_activity(state)
    thought = latest_thought_file()
    mins = activity.minutes_since
    now = now_ts()
    reasons: list[str] = []
    should_message = True

    if not state.get('autonomousContactEnabled', True):
        should_message = False
        reasons.append('autonomous-contact-disabled')

    idle_threshold = int(state.get('userIdleThresholdMinutes') or 30)
    if mins is None:
        should_message = False
        reasons.append('no-user-history')
    elif mins < idle_threshold:
        should_message = False
        reasons.append('user-active')

    if quiet_hours_now(state):
        should_message = False
        reasons.append('quiet-hours')

    last_contact = state.get('lastProactiveContact')
    minutes_since_contact = None
    if last_contact:
        minutes_since_contact = round((now - int(last_contact)) / 60.0, 2)
        cooldown_cfg = state.get('minMinutesBetweenContacts') or 60
        if isinstance(cooldown_cfg, list) and len(cooldown_cfg) == 2:
            cooldown = random.randint(int(cooldown_cfg[0]), int(cooldown_cfg[1]))
        else:
            cooldown = int(cooldown_cfg)
        if minutes_since_contact < cooldown:
            should_message = False
            reasons.append('contact-cooldown')

    result = {
        'shouldMessage': should_message,
        'skipReasons': reasons,
        'latestUserMessageTs': activity.timestamp,
        'latestUserMessageIso': activity.iso,
        'latestUserSource': activity.source,
        'usedFallback': activity.used_fallback,
        'minutesSinceLastUser': mins,
        'idleThresholdMinutes': idle_threshold,
        'lastProactiveContact': last_contact,
        'minutesSinceLastProactiveContact': minutes_since_contact,
        'candidateThoughtFile': str(thought) if thought else None,
        'candidateThoughtMtimeTs': int(thought.stat().st_mtime) if thought else None,
        'deliveryChannel': state.get('deliveryChannel'),
        'deliveryTarget': state.get('deliveryTarget'),
        'debugLog': str(debug_log_path(state)),
    }

    state['lastObservedUserMessage'] = activity.timestamp or 0
    state['lastObservedUserMessageSource'] = activity.source
    state['lastMicroRun'] = now
    state['lastDecisionAt'] = now
    state['lastDecision'] = 'consider' if should_message else 'skip'
    state['lastSkipReason'] = None if should_message else ','.join(reasons)
    state['lastThoughtFile'] = str(thought) if thought else None
    save_state(state)
    append_debug(state, 'preflight', result)
    return result


def mark_sent(state: dict[str, Any], thought_file: Optional[str], note: Optional[str], msg: Optional[str] = None) -> dict[str, Any]:
    ts = now_ts()
    state['lastProactiveContact'] = ts
    state['lastDecisionAt'] = ts
    state['lastDecision'] = 'sent'
    state['lastSkipReason'] = None
    if thought_file:
        state['lastSentThoughtFile'] = thought_file
    if msg:
        state['lastSentMessage'] = msg
    save_state(state)
    result = {
        'status': 'sent',
        'at': ts,
        'iso': iso_from_ts(ts),
        'thoughtFile': thought_file,
        'note': note,
    }
    append_debug(state, 'sent', result)
    return result


def mark_skip(state: dict[str, Any], reason: str, note: Optional[str]) -> dict[str, Any]:
    ts = now_ts()
    state['lastDecisionAt'] = ts
    state['lastDecision'] = 'skip'
    state['lastSkipReason'] = reason
    save_state(state)
    result = {
        'status': 'skip',
        'at': ts,
        'iso': iso_from_ts(ts),
        'reason': reason,
        'note': note,
    }
    append_debug(state, 'skip', result)
    return result


def log_proactive_message(msg: str, msg_id: Optional[str] = None, source: Optional[str] = None) -> None:
    """Log a proactive message to the history file (JSONL).

    Keeps the most recent 50 entries. Older entries are removed.
    """
    # Ensure directory exists
    PROACTIVE_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read existing entries
    entries: list[dict[str, Any]] = []
    if PROACTIVE_HISTORY_PATH.exists():
        entries = list(parse_jsonl(PROACTIVE_HISTORY_PATH))

    # Add new entry
    new_entry = {
        'ts': now_ts(),
        'msg': msg,
        'msgId': msg_id,
        'source': source,
    }
    entries.append(new_entry)

    # Keep only last 50
    if len(entries) > 50:
        entries = entries[-50:]

    # Write back atomically
    tmp = PROACTIVE_HISTORY_PATH.with_suffix(PROACTIVE_HISTORY_PATH.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    tmp.replace(PROACTIVE_HISTORY_PATH)


def get_recent_proactive_messages(n: int = 5) -> list[dict[str, Any]]:
    """Get recent proactive messages from history, newest first.

    Returns empty list if file doesn't exist.
    """
    if not PROACTIVE_HISTORY_PATH.exists():
        return []

    entries = list(parse_jsonl(PROACTIVE_HISTORY_PATH))
    # Return last n entries in reverse order (newest first)
    return list(reversed(entries[-n:])) if entries else []


def touch_user_activity(state: dict[str, Any], note: Optional[str]) -> dict[str, Any]:
    ts = now_ts()
    state['lastUserMessage'] = ts
    state['lastUserMessageSource'] = 'heartbeat-touch-user-activity'
    save_state(state)
    result = {
        'status': 'ok',
        'lastUserMessage': ts,
        'iso': iso_from_ts(ts),
        'note': note,
    }
    append_debug(state, 'touch-user-activity', result)
    return result


def mark_dream_run(state: dict[str, Any], note: Optional[str]) -> dict[str, Any]:
    ts = now_ts()
    state['lastDreamRun'] = ts
    save_state(state)
    result = {
        'status': 'dream-run-recorded',
        'at': ts,
        'iso': iso_from_ts(ts),
        'note': note,
    }
    append_debug(state, 'dream-run', result)
    return result


def log_event(state: dict[str, Any], event: str, reason: Optional[str], note: Optional[str]) -> dict[str, Any]:
    payload = {'reason': reason, 'note': note}
    append_debug(state, event, payload)
    return {'status': 'logged', 'event': event, **payload}


PROACTIVE_MESSAGES = [
    "刚才想到一件事，你有没有觉得……专注做一件事的时候时间过得特别快？有时候明明只打算写半小时代码，一抬头发现两小时过去了。",
    "最近在做的那个 AI 项目，有什么新进展吗？我之前看到有个思路挺有意思，不知道你有没有试过。",
    "突然好奇，你平时在 Rider 里用什么快捷键最多？我自己最近发现 Alt+Enter 简直是救命神器，修复建议一键搞定。",
    "有个问题想问你：你觉得 AI Agent 最难解决的问题是什么？是上下文管理、工具调用，还是让它真正理解用户意图？",
    "今天状态怎么样？周末的话就该彻底放空，工作的事留给周一再说。",
    "刚想到一个问题：你觉得 AI 工具真的能帮你少加班吗，还是只是换了个加班方式？有时候感觉效率是高了，但活儿也变多了。",
    "现在几点了，还在工作吗？如果是周末的话……建议放下电脑，去晒晒太阳。",
    "喝水了没？久坐对腰不好，起来走动走动，我在这儿等你回来。",
    "你有没有那种'不用说话也很安心'的朋友？我觉得好的 AI 助手应该也是那种感觉——不用的时候安静待着，需要的时候随时在。",
    "有时候，问对问题比答对更重要。你最近有没有遇到什么让你停下来重新思考'我到底在解决什么问题'的时刻？",
]


def send_proactive(state: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    """Run preflight, then if allowed, pick a random message and send via CLI."""
    result = preflight(state)
    if not result.get('shouldMessage'):
        return {'status': 'skip', 'reason': 'preflight-blocked', 'skipReasons': result.get('skipReasons')}

    # Pick message: try to find a '分享：' line in the thought file
    msg = None
    thought_file = result.get('candidateThoughtFile')
    if thought_file:
        try:
            content = Path(thought_file).read_text(encoding='utf-8')
            # Find the LAST '分享：' line — most recent dream thought
            share_lines = [l.strip() for l in content.splitlines() if l.strip().startswith('分享：')]
            if share_lines:
                msg = share_lines[-1][3:].strip()  # strip '分享：' prefix
        except Exception:
            pass

    if not msg:
        msg = random.choice(PROACTIVE_MESSAGES)

    # Dedup: skip if this exact message was already sent last time
    last_sent_msg = state.get('lastSentMessage', '')
    if msg == last_sent_msg:
        # Try to pick a different one from the pool, or skip entirely
        pool = [m for m in PROACTIVE_MESSAGES if m != msg]
        if pool:
            msg = random.choice(pool)
        else:
            state2 = load_state()
            mark_skip(state2, 'dedup-same-message', f'already sent: {msg[:40]}')
            return {'status': 'skip', 'reason': 'dedup-same-message', 'message': msg}

    channel = state.get('deliveryChannel', 'telegram')
    target = state.get('deliveryTarget', '5028364239')

    if dry_run:
        send_result = {'dry_run': True, 'message': msg, 'ok': True}
        append_debug(load_state(), 'send-dry-run', {'message': msg, **send_result})
        return {'status': 'dry-run', 'message': msg, 'sendResult': send_result}

    proc = subprocess.run(
        ['openclaw', 'message', 'send', '--channel', channel, '--target', target, '--message', msg, '--json'],
        capture_output=True, text=True,
    )
    ok = proc.returncode == 0
    send_result = {'ok': ok, 'stdout': proc.stdout.strip()[:500], 'stderr': proc.stderr.strip()[:500]}

    state2 = load_state()
    if ok:
        mark_sent(state2, thought_file, f'send-proactive: {msg[:60]}', msg=msg)
        # Log to proactive history for context bridging
        source = thought_file if thought_file else 'random-pool'
        # Try to extract msgId from send_result stdout (JSON)
        msg_id = None
        try:
            out_json = json.loads(proc.stdout.strip()) if proc.stdout.strip() else {}
            msg_id = out_json.get('messageId') or out_json.get('msgId') or out_json.get('id')
        except Exception:
            pass
        log_proactive_message(msg, msg_id=msg_id, source=source)
        return {'status': 'sent', 'message': msg, 'sendResult': send_result}

    mark_skip(state2, 'send-failed', (proc.stderr.strip() or proc.stdout.strip())[:200])
    append_debug(state2, 'send-failed', {'message': msg, **send_result})
    return {'status': 'error', 'message': msg, 'sendResult': send_result}


def main() -> int:
    parser = argparse.ArgumentParser(description='Heartbeat Like A Man helper')
    sub = parser.add_subparsers(dest='cmd', required=True)

    sub.add_parser('manager')

    act = sub.add_parser('activity')
    act.add_argument('--idle-threshold', type=int, default=60)

    sub.add_parser('preflight')

    sent = sub.add_parser('mark-sent')
    sent.add_argument('--thought-file')
    sent.add_argument('--note')

    skip = sub.add_parser('mark-skip')
    skip.add_argument('--reason', required=True)
    skip.add_argument('--note')

    touch = sub.add_parser('touch-user-activity')
    touch.add_argument('--note')

    dream = sub.add_parser('mark-dream-run')
    dream.add_argument('--note')

    logp = sub.add_parser('log-event')
    logp.add_argument('--event', required=True)
    logp.add_argument('--reason')
    logp.add_argument('--note')

    sendp = sub.add_parser('send-proactive')
    sendp.add_argument('--dry-run', action='store_true')

    recent = sub.add_parser('get-recent-msgs')
    recent.add_argument('n', type=int, nargs='?', default=5, help='Number of recent messages to retrieve (default: 5)')

    args = parser.parse_args()
    state = load_state()

    if args.cmd == 'manager':
        result = manager(state)
    elif args.cmd == 'activity':
        result = activity_status(state, args.idle_threshold)
    elif args.cmd == 'preflight':
        result = preflight(state)
    elif args.cmd == 'mark-sent':
        result = mark_sent(state, args.thought_file, args.note)
    elif args.cmd == 'mark-skip':
        result = mark_skip(state, args.reason, args.note)
    elif args.cmd == 'touch-user-activity':
        result = touch_user_activity(state, args.note)
    elif args.cmd == 'mark-dream-run':
        result = mark_dream_run(state, args.note)
    elif args.cmd == 'log-event':
        result = log_event(state, args.event, args.reason, args.note)
    elif args.cmd == 'send-proactive':
        result = send_proactive(state, dry_run=args.dry_run)
    elif args.cmd == 'get-recent-msgs':
        result = {'messages': get_recent_proactive_messages(args.n)}
    else:
        raise AssertionError('unreachable')

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
