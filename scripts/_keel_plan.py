"""Shared plan logic for scripts/keel-plan, scripts/keel-time and scripts/keel-verify.

Sources of truth: docs/sprints/sprint-<N>.md and docs/sprints/deferred.md (YAML frontmatter,
closed schema keel.sprint/1). Derived, never hand-edited: docs/.keel/plan.json and
docs/sprints/README.md. Standard library only.
"""
import glob
import json
import os
import re
import subprocess

UNIT = "AI working hours plus supervision hours"
STATUSES = ("not-started", "in-progress", "done", "dropped")
SOURCES = ("measured", "estimated")


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("keel: not inside a git repository")
    return out.stdout.strip()


def _scalar(text):
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()] if inner else []
    if text in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text.strip("'\"")


def _strip_comment(line):
    return re.sub(r"\s+#.*$", "", line.rstrip("\n"))


def parse_frontmatter(path):
    """Parse the closed keel.sprint/1 frontmatter: top-level scalars plus one list of item maps."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: no frontmatter")
    data, items, current = {}, None, None
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if not line.startswith(" "):
            key, _, value = line.partition(":")
            if value.strip() == "":
                items = []
                data[key.strip()] = items
            else:
                data[key.strip()] = _scalar(value)
            current = None
        elif line.lstrip().startswith("- "):
            current = {}
            items.append(current)
            key, _, value = line.lstrip()[2:].partition(":")
            current[key.strip()] = _scalar(value)
        else:
            key, _, value = line.strip().partition(":")
            current[key.strip()] = _scalar(value)
    return data


def sprint_files(root):
    paths = glob.glob(os.path.join(root, "docs", "sprints", "sprint-*.md"))
    return sorted(paths, key=lambda p: int(re.search(r"sprint-(\d+)\.md$", p).group(1)))


def load(root):
    sprints = []
    for path in sprint_files(root):
        data = parse_frontmatter(path)
        data["path"] = os.path.relpath(path, root)
        data["slices"] = data.get("slices") or []
        sprints.append(data)
    deferred_path = os.path.join(root, "docs", "sprints", "deferred.md")
    deferred = []
    if os.path.exists(deferred_path):
        deferred = parse_frontmatter(deferred_path).get("items") or []
    return sprints, deferred


def _num(value):
    return float(value) if isinstance(value, (int, float)) else 0.0


def _totals(slices):
    live = [s for s in slices if s.get("status") != "dropped"]
    done = [s for s in live if s.get("status") == "done"]
    estimated = sum(_num(s.get("hours")) for s in live)
    done_hours = sum(_num(s.get("hours")) for s in done)
    actual = sum(_num(s.get("actual_hours")) for s in done)
    remaining = sum(_num(s.get("hours")) for s in live if s.get("status") != "done")
    return {
        "estimated_hours": round(estimated, 4),
        "done_hours": round(done_hours, 4),
        "actual_hours": round(actual, 4),
        "remaining_hours": round(remaining, 4),
        "deviation_hours": round(actual - done_hours, 4),
        "percent_done": round(100 * done_hours / estimated, 2) if estimated else 0.0,
        "slices_total": len(live),
        "slices_done": len(done),
    }


def pace(all_slices):
    eligible = [
        s for s in all_slices
        if s.get("status") == "done" and s.get("actual_source") == "measured"
        and _num(s.get("hours")) > 0 and isinstance(s.get("actual_hours"), (int, float))
        and s.get("actual_hours") >= 0
    ]
    est = sum(_num(s["hours"]) for s in eligible)
    act = sum(_num(s["actual_hours"]) for s in eligible)
    factor = act / est if eligible and est else None
    return {"eligible_slices": len(eligible), "eligible_estimated_hours": round(est, 4),
            "eligible_actual_hours": round(act, 4), "pace_factor": factor}


def build(root):
    sprints, deferred = load(root)
    all_slices = [s for sp in sprints for s in sp["slices"]]
    sample = pace(all_slices)
    factor = sample["pace_factor"]

    def project(remaining):
        if remaining == 0:
            return 0.0
        return round(remaining * factor, 4) if factor is not None else None

    out_sprints = []
    for sp in sprints:
        totals = _totals(sp["slices"])
        totals["projected_remaining_hours"] = project(totals["remaining_hours"])
        out_sprints.append({
            "sprint": sp.get("sprint"), "goal": sp.get("goal"), "status": sp.get("status"),
            "path": sp["path"], **totals,
            "slices": [{k: s.get(k) for k in ("id", "title", "status", "hours", "actual_hours",
                                               "actual_source", "depends_on", "criteria")}
                       for s in sp["slices"]],
        })
    totals = _totals(all_slices)
    totals["projected_remaining_hours"] = project(totals["remaining_hours"])
    return {
        "schema": "keel.plan/1",
        "unit": UNIT,
        "contingency_included": False,
        **totals,
        "pace_factor": round(factor, 6) if factor is not None else None,
        "pace_sample": {k: v for k, v in sample.items() if k != "pace_factor"},
        "sprints": out_sprints,
        "deferred": [{k: d.get(k) for k in ("id", "title", "hours", "target", "reason", "depends_on")}
                     for d in deferred],
        "deferred_hours": round(sum(_num(d.get("hours")) for d in deferred), 4),
    }


def render_json(plan):
    return json.dumps(plan, indent=2, ensure_ascii=False) + "\n"


def fmt(hours):
    if hours is None:
        return "—"
    text = f"{hours:.2f}".rstrip("0").rstrip(".")
    return text or "0"


def render_index(plan):
    rows = ["# Sprint plan — index", "",
            "> GENERATED by `scripts/keel-plan` from the sprint files. Never edit by hand.",
            f"> Every figure is {UNIT}. Contingency and `deferred.md` are not included.", "",
            "| Sprint | Goal | Status | Slices done | Estimated h | Remaining h | Done % |",
            "|---|---|---|---|---|---|---|"]
    for sp in plan["sprints"]:
        rows.append(f"| [{sp['sprint']}](sprint-{sp['sprint']}.md) | {sp['goal']} | {sp['status']} | "
                    f"{sp['slices_done']}/{sp['slices_total']} | {fmt(sp['estimated_hours'])} | "
                    f"{fmt(sp['remaining_hours'])} | {fmt(sp['percent_done'])} |")
    rows.append(f"| **Total** | | | {plan['slices_done']}/{plan['slices_total']} | "
                f"**{fmt(plan['estimated_hours'])}** | **{fmt(plan['remaining_hours'])}** | "
                f"{fmt(plan['percent_done'])} |")
    rows += ["", f"Backlog (`deferred.md`): {len(plan['deferred'])} items, "
                 f"{fmt(plan['deferred_hours'])} h — what a later version would cost, not in the total.", ""]
    return "\n".join(rows)


def write(root):
    plan = build(root)
    os.makedirs(os.path.join(root, "docs", ".keel"), exist_ok=True)
    with open(os.path.join(root, "docs", ".keel", "plan.json"), "w", encoding="utf-8") as handle:
        handle.write(render_json(plan))
    with open(os.path.join(root, "docs", "sprints", "README.md"), "w", encoding="utf-8") as handle:
        handle.write(render_index(plan))
    return plan


def left_block(plan):
    lines = []
    for sp in plan["sprints"]:
        pending = [s for s in sp["slices"] if s["status"] not in ("done", "dropped")]
        if not pending:
            continue
        lines.append(f"Sprint {sp['sprint']} — {sp['goal']}: {len(pending)} slices pending, "
                     f"{fmt(sp['remaining_hours'])} h left")
    lines.append(f"Total left: {fmt(plan['remaining_hours'])} h of AI working time plus supervision "
                 f"(contingency not included)")
    sign = "+" if plan["deviation_hours"] >= 0 else "−"
    pct = (100 * plan["deviation_hours"] / plan["done_hours"]) if plan["done_hours"] else 0.0
    lines.append(f"So far: {plan['slices_done']} slices done, {fmt(plan['done_hours'])} h estimated, "
                 f"{fmt(plan['actual_hours'])} h actual ({sign}{fmt(abs(plan['deviation_hours']))} h, "
                 f"{sign}{fmt(abs(pct))} %)")
    lines.append(projection_line(plan))
    return "\n".join(lines)


def projection_line(plan):
    sample = plan["pace_sample"]
    if plan["projected_remaining_hours"] is None:
        return "Projection if the observed pace continues: unavailable — no measured completed work"
    note = " — provisional sample" if sample["eligible_slices"] < 5 else ""
    factor = plan["pace_factor"] if plan["pace_factor"] is not None else 1.0
    return (f"Projection if the observed pace continues: {fmt(plan['projected_remaining_hours'])} h left "
            f"(factor {factor:.4f}; {sample['eligible_slices']} measured slices{note})")


def set_slice_fields(root, slice_id, fields):
    """Rewrite scalar fields of one slice inside its sprint file's frontmatter. Returns the path."""
    for path in sprint_files(root):
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
        start = next((i for i, l in enumerate(lines) if re.match(rf"\s+- id:\s*{re.escape(slice_id)}\s*$", l)), None)
        if start is None:
            continue
        end = start + 1
        while end < len(lines) and not re.match(r"\s+- id:", lines[end]) and lines[end].strip() != "---":
            end += 1
        for key, value in fields.items():
            for i in range(start + 1, end):
                if re.match(rf"\s+{key}:", lines[i]):
                    indent = re.match(r"\s*", lines[i]).group(0)
                    lines[i] = f"{indent}{key}: {value}"
                    break
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
        return path
    raise SystemExit(f"keel: slice {slice_id} is not in any sprint file — add it to the plan first")


def set_sprint_status(path, status):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            break
        if line.startswith("status:"):
            lines[i] = f"status: {status}"
            break
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def find_slice(plan, slice_id):
    for sp in plan["sprints"]:
        for s in sp["slices"]:
            if s["id"] == slice_id:
                return sp, s
    return None, None
