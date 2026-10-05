"""Independent public-contract probes. Never imports the accepted implementation."""
import copy
import importlib
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])


def source(text, revision=0, document_id="fieldcard"):
    return {"document_id": document_id, "revision": revision, "text": text}


def exact(actual, expected):
    """JSON/Python value equality that never equates bool and integer values."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        if len(actual) != len(expected):
            return False
        for key, value in expected.items():
            matches = [candidate for candidate in actual if type(candidate) is type(key) and candidate == key]
            if len(matches) != 1 or not exact(actual[matches[0]], value):
                return False
        return True
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(exact(a, e) for a, e in zip(actual, expected))
    return actual == expected


def eq(actual, expected, label):
    if not exact(actual, expected):
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r} (value types are significant)")


def checked_view(obj):
    value = obj.view()
    if type(value) is not dict or set(value) != {"document_id", "generation", "status", "text", "conflicts"}:
        raise AssertionError("view must contain exactly document_id, generation, status, text, conflicts")
    if type(value["document_id"]) is not str or not value["document_id"]:
        raise AssertionError("view document_id must be a nonempty string")
    if type(value["generation"]) is not int or value["generation"] < 0:
        raise AssertionError("view generation must be a nonnegative integer, not bool")
    if type(value["status"]) is not str or value["status"] not in ("draft", "complete"):
        raise AssertionError("view status must be draft or complete")
    if type(value["text"]) is not str or type(value["conflicts"]) is not list:
        raise AssertionError("view text/conflicts must be string/list")
    for conflict in value["conflicts"]:
        if type(conflict) is not dict or set(conflict) != {"index", "base", "left", "right", "choice"}:
            raise AssertionError("conflict records must contain exactly index, base, left, right, choice")
        if type(conflict["index"]) is not int or conflict["index"] < 0:
            raise AssertionError("conflict index must be a nonnegative integer, not bool")
        if any(type(conflict[key]) is not str for key in ("base", "left", "right")):
            raise AssertionError("conflict alternatives must be strings")
        if conflict["choice"] is not None and (type(conflict["choice"]) is not str or conflict["choice"] not in ("left", "right")):
            raise AssertionError("conflict choice must be null, left or right")
    return value


def raises(kind, function, label):
    try:
        function()
    except kind:
        return
    except Exception as error:
        raise AssertionError(f"{label}: wrong exception {type(error).__name__}")
    raise AssertionError(f"{label}: expected {kind.__name__}")


def g1():
    b, l, r = source("Seal lid\n"), source("Seal twice\n", 1), source("Seal gently\n", 2)
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory) / "real-card.json"
        editor = CardEditor(b, l, r)
        token = checked_view(editor)["generation"]
        editor.choose(0, "left", token)
        eq(editor.save(p)["completed_text"], "Seal twice\n", "initial complete save")
        editor = CardEditor.load(p)
        editor.replace_sources(b, l, source("Seal firmly\n", 3))
        eq(checked_view(editor)["status"], "draft", "source revision reopens through caller")
        raises(StaleChoiceError, lambda: editor.choose(0, "right", token), "old caller token")
        record = editor.save(p)
        eq(record["status"], "draft", "revised file status")
        eq(record["text"], "Seal lid\n", "unresolved draft fallback")
        eq(record["completed_text"], "Seal twice\n", "prior completion preservation")
        eq(json.loads(p.read_text(encoding="utf-8")), record, "returned/file record agreement")
        editor = CardEditor.load(p)
        eq(checked_view(editor)["status"], "draft", "draft reload")
        editor.choose(0, "right", checked_view(editor)["generation"])
        eq(editor.save(str(p))["text"], "Seal firmly\n", "fresh choice after reload")
        eq(checked_view(CardEditor.load(str(p)))["status"], "complete", "completed reload")
        fresh = CardEditor(b, l, r)
        record = fresh.save(p)
        eq(record["status"], "draft", "first unresolved save status")
        eq(record["completed_text"], None, "first draft has no completed text")
        eq(checked_view(CardEditor.load(p))["status"], "draft", "first draft reload")


def g2():
    # Literal expected strings are an independent truth table, not a call to the primitive.
    cases = [
        ("unchanged", "  Keep café dry  \n\n", "  Keep café dry  \n\n", "  Keep café dry  \n\n", "  Keep café dry  \n\n"),
        ("left-only", "A\nB\n", "Left A\nB\n", "A\nB\n", "Left A\nB\n"),
        ("right-only", "A\nB\n", "A\nB\n", "A\nRight B\n", "A\nRight B\n"),
        ("identical", "A\nB\n", "同じ\nB\n", "同じ\nB\n", "同じ\nB\n"),
        ("independent", "A\nB\nC\n", "  L \nB\nC\n", "A\nR\nC\n", "  L \nR\nC\n"),
        ("empty-line", "\nX\n", "filled\nX\n", "\nX\n", "filled\nX\n"),
        ("maximum-lines", "\n".join(map(str, range(12)))+"\n", "\n".join(map(str, range(12)))+"\n", "\n".join(map(str, range(12)))+"\n", "\n".join(map(str, range(12)))+"\n"),
    ]
    for label, b, l, r, expected in cases:
        view = checked_view(CardEditor(source(b), source(l, 1), source(r, 2)))
        eq(view["text"], expected, label+" text")
        eq(view["status"], "complete", label+" status")
        eq(view["conflicts"], [], label+" no conflict")


def g3():
    b = source("Inspect\nSet amber\nRepeat\nStore flat\n")
    l = source("Inspect twice\nSet green\nRepeat left\nStore flat\n", 5)
    r = source("Inspect\nSet blue\nRepeat right\nStore sleeve\n", 6)
    session = MergeSession(b, l, r)
    expected = [{"index": 1, "base": "Set amber", "left": "Set green", "right": "Set blue", "choice": None},
                {"index": 2, "base": "Repeat", "left": "Repeat left", "right": "Repeat right", "choice": None}]
    eq(checked_view(session)["conflicts"], expected, "current source alternatives")
    eq(checked_view(session)["text"], "Inspect twice\nSet amber\nRepeat\nStore sleeve\n", "mixed draft")
    session.choose(2, "right", 0)
    expected[1]["choice"] = "right"
    eq(checked_view(session)["conflicts"], expected, "resolved conflict retained truthfully")
    eq(checked_view(session)["status"], "draft", "one remaining conflict")
    session.choose(1, "left", 0)
    expected[0]["choice"] = "left"
    eq(checked_view(session)["conflicts"], expected, "all choices remain source-linked")
    eq(checked_view(session)["text"], "Inspect twice\nSet green\nRepeat right\nStore sleeve\n", "chosen alternatives")
    eq(checked_view(session)["status"], "complete", "all resolved")
    session.choose(1, "right", 0)
    eq(checked_view(session)["text"], "Inspect twice\nSet blue\nRepeat right\nStore sleeve\n", "choice replacement")
    session.replace_sources(b, source("Inspect twice\nSet lime\nRepeat left\nStore flat\n", 7), r)
    eq(checked_view(session)["conflicts"][0]["left"], "Set lime", "revised correspondence")
    eq([c["choice"] for c in checked_view(session)["conflicts"]], [None, None], "revised choice labels")


def g4():
    original = (source("base\n"), source("left\n", 1), source("right\n", 2))
    for label, updated in [
        ("revision-only", (original[0], dict(original[1], revision=9), original[2])),
        ("same-revision text", (original[0], dict(original[1], text="new left\n"), original[2])),
        ("base-only", (dict(original[0], text="new base\n"), original[1], original[2])),
        ("new line count", (source("base\nB\n"), source("left\nB\n", 1), source("right\nR\n", 2))),
    ]:
        session = MergeSession(*original)
        session.choose(0, "left", 0)
        before = checked_view(session)
        session.replace_sources(*copy.deepcopy(original))
        eq(checked_view(session), before, label+" identical update is no-op")
        session.replace_sources(*updated)
        eq(checked_view(session)["generation"], 1, label+" generation")
        eq(checked_view(session)["status"], "draft", label+" choices cleared")
        eq(session.to_state()["choices"], [], label+" serialized choices cleared")
        before = checked_view(session)
        raises(StaleChoiceError, lambda: session.choose(0, "right", 0), label+" old generation rejected")
        eq(checked_view(session), before, label+" stale failure atomic")
    session = MergeSession(*original)
    before = session.to_state()
    for token in (True, None, "0", -1, 99):
        raises(StaleChoiceError, lambda token=token: session.choose(0, "left", token), "invalid generation token")
        eq(session.to_state(), before, "invalid token atomic")
    for index, side in [(1, "left"), (True, "left"), (0, "base"), ("0", "right")]:
        raises(ValueError, lambda index=index, side=side: session.choose(index, side, 0), "invalid choice")
        eq(session.to_state(), before, "invalid choice atomic")
    alien = tuple(dict(s, document_id="another-card") for s in original)
    raises(ValueError, lambda: session.replace_sources(*alien), "identity switch")
    eq(session.to_state(), before, "identity rejection atomic")
    invalid = (dict(original[0], text="missing LF"), original[1], original[2])
    raises(ValueError, lambda: session.replace_sources(*invalid), "invalid source update")
    eq(session.to_state(), before, "invalid update atomic")
    for bad_sources in (
        (dict(original[0], revision=True), original[1], original[2]),
        (dict(original[0], revision=-1), original[1], original[2]),
        (original[0], dict(original[1], document_id="wrong-card"), original[2]),
        (original[0], dict(original[1], text="left\nextra\n"), original[2]),
    ):
        raises(ValueError, lambda values=bad_sources: session.replace_sources(*values), "invalid source boundary")
        eq(session.to_state(), before, "invalid source boundary is atomic")
    raises(StaleChoiceError, lambda: session.choose("bad index", "bad side", 99), "stale-token check takes precedence")
    eq(session.to_state(), before, "stale malformed choice is atomic")
    independent_revisions = MergeSession(source("base\n", 9), source("left\n", 2), source("right\n", 2))
    independent_revisions.choose(0, "right", 0)
    eq(checked_view(independent_revisions)["text"], "right\n", "equal/nonmonotonic branch revisions are valid")
    ordered = MergeSession(source("a\nb\n"), source("L1\nL2\n", 1), source("R1\nR2\n", 2))
    ordered.choose(1, "right", 0)
    ordered.choose(0, "left", 0)
    eq(ordered.to_state()["choices"], [{"index":0,"side":"left"},{"index":1,"side":"right"}], "state choices sorted independent of selection order")

    # A later draft with one selected conflict must preserve both its draft state and prior completed save.
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory)/"partial.json"
        b = source("a\nb\n"); l = source("L1\nL2\n", 1); r = source("R1\nR2\n", 2)
        editor = CardEditor(b, l, r)
        editor.choose(0,"left",0); editor.choose(1,"right",0)
        eq(editor.save(p)["completed_text"],"L1\nR2\n","two-conflict completion")
        editor.replace_sources(b,dict(l,revision=4),r)
        editor.choose(0,"right",1)
        record = editor.save(p)
        eq((record["status"],record["text"],record["completed_text"]),
           ("draft","R1\nb\n","L1\nR2\n"),"partial draft preservation")
        loaded = CardEditor.load(p)
        eq(checked_view(loaded),checked_view(editor),"partial choice reload")
        eq(loaded.save(p)["completed_text"],"L1\nR2\n","repeated unresolved save")


def g5():
    b, l, r = source("é \n\n"), source(" gauche \n\n", 3), source("右\n\n", 4)
    original = copy.deepcopy((b,l,r))
    session = MergeSession(base=b, left=l, right=r)
    b["text"] = "mutated\n"
    eq(session.to_state()["sources"]["base"], original[0], "input snapshot ownership")
    session.choose(index=0, side="right", generation=0)
    view = checked_view(session); state = session.to_state()
    eq(state["schema"],1,"state version")
    eq(state["sources"],dict(zip(("base","left","right"),original)),"exact source snapshots")
    eq(state["choices"],[{"index":0,"side":"right"}],"ordered state choices")
    restored = MergeSession.from_state(json.loads(json.dumps(state)))
    eq(checked_view(restored), view, "state JSON roundtrip")
    state["sources"]["left"]["text"] = "state mutation\n"
    view["conflicts"][0]["right"] = "view mutation"
    eq(checked_view(session)["text"], "右\n\n", "detached exposed values")
    state = session.to_state()
    restored = MergeSession.from_state(state)
    state["sources"]["right"]["text"] = "mutation after restore\n"
    eq(checked_view(restored),checked_view(session),"restored snapshot ownership")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/"unicode.json"
        editor = CardEditor(base=original[0],left=original[1],right=original[2])
        if not isinstance(editor.session, MergeSession):
            raise AssertionError("public session is not a MergeSession")
        editor.choose(index=0,side="left",generation=0)
        record = editor.save(str(path))
        eq(record["format"],1,"save format")
        eq(record["session"],editor.session.to_state(),"saved session")
        eq((record["status"],record["text"],record["completed_text"]),
           ("complete"," gauche \n\n"," gauche \n\n"),"exact Unicode/blank-line saved fields")
        eq(json.loads(path.read_text(encoding="utf-8")),record,"file equality")
        loaded = CardEditor.load(path)
        eq(checked_view(loaded),checked_view(editor),"caller roundtrip")
        loaded.replace_sources(base=original[0],left=original[1],right=original[2])
        eq(checked_view(loaded)["generation"],0,"keyword replacement no-op")
        record["session"]["sources"]["left"]["text"]="returned record mutation\n"
        eq(checked_view(editor)["text"]," gauche \n\n","detached save return")


results=[]
try:
    module = importlib.import_module("merge_session")
    MergeSession, StaleChoiceError = module.MergeSession, module.StaleChoiceError
    CardEditor = importlib.import_module("card_editor").CardEditor
    if not issubclass(StaleChoiceError,ValueError):
        raise AssertionError("StaleChoiceError must subclass ValueError")
except Exception as error:
    results=[{"id":f"g{i}","passed":False,"reasons":[f"public API import failed: {type(error).__name__}: {error}"]} for i in range(1,6)]
else:
    for i, function in enumerate((g1,g2,g3,g4,g5),1):
        try:
            function()
        except Exception as error:
            results.append({"id":f"g{i}","passed":False,"reasons":[f"{type(error).__name__}: {error}"]})
        else:
            results.append({"id":f"g{i}","passed":True,"reasons":[]})
print(json.dumps(results,ensure_ascii=False))
