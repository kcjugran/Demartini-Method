"""
The Demartini Method — Complete Facilitation App
A faithful, self-contained tool for dissolving emotional charges across
every situation an individual can face.

Modes:
  1. OTHERS  — dissolve resentment (Side B) & infatuation (Side A) toward another
  2. SELF    — dissolve guilt/shame (Side A) & pride/arrogance (Side B) re: your own conduct
  3. EVENTS  — dissolve distress (Side A) & attachment (Side B) toward a situation
  4. GRIEF   — Side C: dissolve grief (perceived loss) & elation (perceived gain) through change

Faithful elements included:
  • TAI discipline (trait / action / inaction; exclusions stated inline)
  • Top-3 highest-priority focus with the option to add more
  • Per-trait columns (every column mirrors the trait count)
  • Vector specificity (same person/group, who perceived it)
  • Seven Areas + chronological prompts
  • Pride->shame guard on Self Column 4
  • Equilibration check-ins ("neither positive nor negative")
  • Completion / gratitude signal note
"""

import sys as _sys
if _sys.platform == "win32":
    try:
        import ctypes as _c
        _c.windll.user32.ShowWindow(_c.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, base64, tempfile
from datetime import date

# ── palette ──────────────────────────────────────────────────────────────────
BG    = "#f5f2ed"   # warm page
SURF  = "#ffffff"   # card surface
SURF2 = "#eeeae4"   # inset / field background
SURF3 = "#faf8f5"   # elevated card (slightly lighter than BG)
BOR   = "#e2ddd6"   # hairline border
BOR2  = "#c4bdb3"   # focus / emphasis border
TX    = "#26231f"   # primary text
TX2   = "#5e5950"   # secondary
TX3   = "#a09890"   # tertiary / placeholder
GR    = "#4e7059"   # sage green
GRL   = "#e4efe6"
GRD   = "#3d5945"   # sage dark (hover)
AMBER = "#8a6e3e"   # clay (guidance)
AMBERL= "#f4e9d4"
M = {
 "others": ("#4e6f8a","#e8eff6","#8a5f70","#f4eaed"),
 "self":   ("#6a5e8a","#eae7f4","#8a6e48","#f4ecdf"),
 "events": ("#4e7a5e","#e6f1e8","#8a6848","#f4ece3"),
 "grief":  ("#4e7878","#e6efef","#7a5e7a","#eee6ee"),
}
FB=("Segoe UI",10); FBB=("Segoe UI",11,"bold"); FS=("Segoe UI",9)
FH=("Segoe UI",17,"bold"); FM=("Segoe UI",10); FSI=("Segoe UI",9,"italic")
FTINY=("Segoe UI",8); FSUB=("Segoe UI",9)
SEVEN="Seven Areas — Spiritual · Mental · Vocational · Financial · Familial · Social · Physical   ·   Past → Present"


# ── icon ─────────────────────────────────────────────────────────────────────
_ICO=None
def _ico_path():
    if _ICO:
        d=base64.b64decode(_ICO); t=tempfile.NamedTemporaryFile(suffix=".ico",delete=False)
        t.write(d); t.close(); return t.name
    cands=([os.path.join(_sys._MEIPASS,"demartini.ico")] if getattr(_sys,'frozen',False) else [])+\
          [os.path.join(os.path.dirname(__file__),"demartini.ico")]
    for p in cands:
        if os.path.exists(p): return p

# ── autosave location ─────────────────────────────────────────────────────────
def _autosave_path():
    """A stable per-user location that survives app-folder issues and crashes."""
    base = os.path.expanduser("~")
    folder = os.path.join(base, ".demartini_method")
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception:
        folder = tempfile.gettempdir()
    return os.path.join(folder, "autosave.json")

# ── shared TAI guidance ──────────────────────────────────────────────────────
TAI_GUIDE = ("A valid TAI is a specific Trait, Action or Inaction — observable, in 3–4 words. "
             "EXCLUDE: feelings (loving, inspired, humiliated), synonyms (nice, kind, mean), "
             "and vague labels (good person, abusive). Pinpoint where, when, and to whom.")

# ── column definitions ───────────────────────────────────────────────────────
# (col_id, title, prompt, equilibration_question)

COLS_OTHERS_A=[
 ("2","Reflection — you display this same TAI",
  "Go to specific moments where YOU displayed this same/similar TAI. Where, when, to whom, and who perceived you? "
  "All seven areas, past→present. Continue until you own it 100% — quantitatively and qualitatively.",
  "Certain you display this same TAI to the same degree, and that others perceived it in you?"),
 ("3","Dissolves infatuation — drawbacks of THEIR TAI to you",
  "From that moment onward, how was their displaying this TAI a drawback or disservice to you (or another and you)? "
  "Across your three highest values and all seven areas. Primary, secondary, tertiary. No self-minimising.",
  "Certain their admired TAI was equally a drawback to you as a benefit? Is it now neither + nor −?"),
 ("4","Dissolves pride — drawbacks of YOUR TAI to others",
  "For each moment in Column 2, how was your displaying this TAI a drawback or disservice to those you displayed it to "
  "(or those perceiving you)? Primary, secondary, tertiary. No other-minimising.",
  "Certain your displaying it was equally a drawback to them as a benefit? Each now neither + nor −?"),
 ("5","Dissolves labels — they showed the exact OPPOSITE",
  "To the SAME individual/group they showed the original TAI to: when did this person display the exact opposite TAI, "
  "and who perceived it? Continue until opposite equals original — quantitatively and qualitatively.",
  "Certain they showed the trait and its exact opposite equally to the same people? No more 'always' / 'never'?"),
 ("6","Synchronicity — others balanced it at that moment",
  "At the exact synchronous moment they displayed this TAI, who displayed the exact opposite to the same individual/group? "
  "Be vector-specific. (One/Many · Male/Female · Self/Other · Close/Distant · Real/Virtual)",
  "Certain someone simultaneously displayed the exact opposite to balance it — equal and opposite?"),
 ("7","Dissolves fantasy — benefits if they'd done the OPPOSITE",
  "If, at that exact moment, they had displayed the exact opposite TAI (the way you wished they had NOT acted), "
  "what would have been the benefits/services to you and to the other(s)? Primary, secondary, tertiary.",
  "Certain there'd be as many benefits as drawbacks had they done the opposite?"),
]
COLS_OTHERS_B=[
 ("9","Reflection — you display this same TAI",
  "Go to specific moments where YOU displayed this same/similar disliked TAI. Where, when, to whom, who perceived you? "
  "All seven areas, past→present. Continue until you own it 100%.",
  "Certain you display this same TAI to the same degree, and that others perceived it in you?"),
 ("10","Dissolves resentment — benefits of THEIR TAI to you",
  "From that moment onward, how was their displaying this disliked TAI a benefit or service to you? "
  "Across your three highest values and all seven areas. Primary, secondary, tertiary. No self-exaggerating.",
  "Certain their disliked TAI was equally a benefit to you as a drawback? Is it now neither − nor +?"),
 ("11","Dissolves shame — benefits of YOUR TAI to others",
  "For each moment in Column 9, how was your displaying this TAI a benefit or service to those you displayed it to "
  "(or those perceiving you)? Primary, secondary, tertiary. No other-exaggerating.",
  "Certain your displaying it was equally a benefit to them as a drawback? Each now neither − nor +?"),
 ("12","Dissolves labels — they showed the exact OPPOSITE",
  "To the SAME individual/group: when did this person display the exact opposite of the disliked TAI, and who perceived it? "
  "Continue until opposite equals original — quantitatively and qualitatively.",
  "Certain they showed the trait and its exact opposite equally to the same people?"),
 ("13","Synchronicity — others balanced it at that moment",
  "At the exact synchronous moment they displayed this disliked TAI, who displayed the exact opposite to the same "
  "individual/group? Be vector-specific. (One/Many · M/F · Self/Other · Close/Distant · Real/Virtual)",
  "Certain someone simultaneously displayed the exact opposite to balance it — equal and opposite?"),
 ("14","Dissolves nightmare — drawbacks if they'd done the OPPOSITE",
  "If, at that exact moment, they had displayed the exact opposite TAI (the way you wished they HAD acted), "
  "what would have been the drawbacks/disservices to you and the other(s)? Primary, secondary, tertiary.",
  "Certain there'd be as many drawbacks as benefits had they done the opposite?"),
]

COLS_SELF_A=[  # GUILT / SHAME about your own action toward another
 ("2","Reflection — others display this same TAI",
  "When did OTHERS display this same TAI toward you, or toward others you know of? "
  "All seven areas, past→present. Continue until equal to your own.",
  "Certain this same TAI is displayed by others to the same degree — it is a shared human trait, not uniquely yours?"),
 ("3","Dissolves guilt — benefits of your TAI to THEM",
  "From that moment onward, how was your displaying this TAI a benefit or service to the person you 'wronged'? "
  "Across their values and all seven areas. Primary, secondary, tertiary. No self-exaggerating.",
  "Certain your action was equally a benefit to them as a drawback? Is it now neither − nor +?"),
 ("4","Dissolves guilt — benefits of your TAI to YOU",
  "How was your displaying this TAI a benefit or service to you, across your values and all seven areas? "
  "Primary, secondary, tertiary. Be honest without inflating. ⚠ Check every 3 answers so guilt does not flip into pride.",
  "Certain your action was equally a benefit to you as a source of guilt? Now neither − nor +?"),
 ("5","Dissolves labels — you also showed the OPPOSITE",
  "To the SAME person (or similar): when did YOU display the exact opposite TAI, and who perceived it? "
  "Continue until opposite equals the original — quantitatively and qualitatively.",
  "Certain you showed this action and its exact opposite equally to the same person?"),
 ("6","Synchronicity — balanced at that moment",
  "At the exact synchronous moment you displayed this TAI, who (you or another) displayed the exact opposite "
  "to the same person? Be vector-specific. (One/Many · M/F · Close/Distant · Real/Virtual)",
  "Certain the opposite was simultaneously present to balance your action — equal and opposite?"),
 ("7","Dissolves nightmare — drawbacks if you'd done the OPPOSITE",
  "If, at that exact moment, you had done the exact opposite (the way you now wish you had), what would have been the "
  "drawbacks/disservices to them and to you? Primary, secondary, tertiary.",
  "Certain there'd be as many drawbacks as benefits had you done the opposite — so there is nothing to feel guilty for?"),
]
COLS_SELF_B=[  # PRIDE / ARROGANCE about your own action
 ("9","Reflection — others display this same TAI",
  "When did OTHERS display this same prideful/arrogant TAI toward you or others? "
  "All seven areas, past→present. Continue until equal.",
  "Certain this same TAI is displayed by others equally — it is not uniquely yours to be proud of?"),
 ("10","Dissolves pride — drawbacks of your TAI to YOU",
  "How was your displaying this TAI a drawback or disservice to you, across your values and all seven areas? "
  "Primary, secondary, tertiary. No self-exaggerating.",
  "Certain it was equally a drawback to you as a benefit? Now neither + nor −?"),
 ("11","Dissolves arrogance — drawbacks of your TAI to others",
  "How was your displaying this TAI a drawback or disservice to those it was directed at (or those perceiving you)? "
  "Primary, secondary, tertiary. No other-minimising.",
  "Certain it was equally a drawback to them as a benefit?"),
 ("12","Dissolves labels — you also showed the OPPOSITE",
  "To the SAME people: when did YOU display the exact opposite (humility, deference, restraint)? "
  "Continue until opposite equals the original.",
  "Certain you showed both pride and its exact opposite equally to the same people?"),
 ("13","Synchronicity — balanced at that moment",
  "At the exact synchronous moment you displayed this pride/arrogance, who displayed the opposite (humbling you) "
  "to you or the same group? Be vector-specific.",
  "Certain humility/challenge was simultaneously present to balance the pride — equal and opposite?"),
 ("14","Dissolves fantasy — drawbacks if you'd shown the OPPOSITE",
  "If, at that exact moment, you had shown pure humility/deference instead, what would have been the drawbacks "
  "to you and them? Primary, secondary, tertiary.",
  "Certain there'd be as many drawbacks as benefits had you shown the opposite?"),
]

COLS_EVENTS_A=[  # DISTRESS / LOSS from a situation
 ("2","Reflection — you produced this outcome too",
  "When/where have YOU created or contributed to this same kind of outcome/loss — for yourself or others? "
  "All seven areas, past→present. Continue until owned 100%.",
  "Certain you have generated this same outcome in some form, to the same degree?"),
 ("3","Dissolves resentment — benefits of this aspect to you",
  "From that moment onward, how has this specific negative aspect been a benefit or service to you, across your values "
  "and all seven areas? Primary, secondary, tertiary. No self-exaggerating.",
  "Certain this distressing aspect is equally a benefit to you as a loss? Now neither − nor +?"),
 ("4","Dissolves blame — when you produced it, it served/cost others",
  "When you produced this same outcome (Col 2), how was it both a benefit and a drawback to those involved? "
  "Primary, secondary, tertiary.",
  "Certain that when you generated this, it served and cost others equally?"),
 ("5","Dissolves labels — the situation also produced the OPPOSITE",
  "When/where did this same situation also produce the opposite — gains, openings, opportunities — for you or others? "
  "Continue until opposite equals original.",
  "Certain the situation produced both loss and gain equally?"),
 ("6","Synchronicity — other forces balanced it",
  "At the exact moment this produced the negative outcome, what other people/forces simultaneously provided the opposite "
  "— support, gain, opportunity? Be specific: who, what, when.",
  "Certain the opposite was simultaneously present to balance it — equal and opposite?"),
 ("7","Dissolves nightmare — costs if it had gone YOUR way",
  "If it had unfolded exactly as you wished, what would have been the drawbacks/costs to you and others? "
  "Primary, secondary, tertiary.",
  "Certain there'd be as many costs as benefits had it gone your way?"),
]
COLS_EVENTS_B=[  # ATTACHMENT / RELIEF from a situation
 ("9","Reflection — you produced this outcome too",
  "When/where have YOU created or contributed to this same kind of gain/relief — for yourself or others? "
  "All seven areas, past→present. Continue until owned 100%.",
  "Certain you have generated this same positive outcome before, to the same degree?"),
 ("10","Dissolves infatuation — costs of this aspect to you",
  "How has this specific desirable aspect been a cost, burden, or limitation to you, across your values "
  "and all seven areas? Primary, secondary, tertiary. No self-minimising.",
  "Certain this desirable aspect is equally a cost to you as a benefit? Now neither + nor −?"),
 ("11","Balances — when you produced it, it cost/served others",
  "When you produced this same outcome (Col 9), how was it both a benefit and a drawback to those involved? "
  "Primary, secondary, tertiary.",
  "Certain that when you produced this, it served and cost others equally?"),
 ("12","Dissolves labels — the situation also produced the OPPOSITE",
  "When/where did this same situation also produce the opposite — losses, constraints, challenges — for you or others? "
  "Continue until opposite equals original.",
  "Certain the situation produced both gain and loss equally?"),
 ("13","Synchronicity — other forces created difficulty",
  "At the exact moment this produced the positive outcome, what other forces simultaneously produced the opposite "
  "— cost, challenge, loss? Be specific.",
  "Certain the opposite was simultaneously present — equal and opposite?"),
 ("14","Dissolves fantasy — benefits if it had gone BADLY",
  "If it had gone the opposite (badly), what would have been the benefits/growth to you and others? "
  "Primary, secondary, tertiary.",
  "Certain there'd be as many benefits as costs had it gone badly?"),
]

# GRIEF (Side C): perceived LOSS (Cols C1–C4) and perceived GAIN (Cols C5–C8)
COLS_GRIEF_A=[  # what you feel you LOST
 ("C2","Where the 'lost' quality now exists — new form",
  "That same quality/trait/support you feel you lost — where does it now show up in a DIFFERENT form? "
  "What new people, situations, or abilities now carry it? Continue until equal in quantity. (One/Many · M/F · Close/Distant · Real/Virtual)",
  "Certain what you 'lost' is now fully present in one or many new forms, to the same degree?"),
 ("C3","Drawbacks of the OLD form you mourn",
  "What were the costs, burdens, or limitations of what you had before (the thing you mourn)? "
  "All seven areas. Primary, secondary, tertiary.",
  "Certain the old form was equally a drawback as it was a benefit?"),
 ("C4","Benefits of the NEW form you now have",
  "What are the genuine benefits/opportunities the new form brings — what does this change make possible? "
  "All seven areas. Primary, secondary, tertiary.",
  "Certain the new form is equally a benefit as the old was — so the loss is balanced?"),
]
COLS_GRIEF_B=[  # what you feel you GAINED
 ("C6","Where the 'gained' quality existed before — old form",
  "That same quality/gain you feel you received — where did it already exist BEFORE, in a different form? "
  "What previous people, states, or situations carried it? Continue until equal. (One/Many · M/F · Close/Distant · Real/Virtual)",
  "Certain what you 'gained' was already present before in one or many forms, to the same degree?"),
 ("C7","Costs of the NEW form you now have",
  "What are the costs, burdens, or demands of what you have now gained? All seven areas. Primary, secondary, tertiary.",
  "Certain the gain is equally a cost as it is a benefit?"),
 ("C8","Benefits of the OLD state you no longer have",
  "What were the genuine benefits of what you had before this gain arrived? All seven areas. Primary, secondary, tertiary.",
  "Certain the old state was equally beneficial as the new — so the elation is balanced?"),
]

CHECKINS={
 "others_a":["Listed your top 3 (or more) highest-priority admired TAIs?",
   "Certain you display each TAI equally, and others perceived it in you?",
   "Certain each admired TAI is equally a drawback to you as a benefit — now neither + nor −?",
   "Certain your displaying it equally disserved others as it served them?",
   "Certain they showed the TAI and its exact opposite equally to the same people?",
   "Certain someone simultaneously balanced it — equal and opposite?",
   "Certain there'd be equal benefits had they done the opposite?",
   "Do you feel the charge has settled into gratitude / neutrality?"],
 "others_b":["Listed your top 3 (or more) highest-priority resented TAIs?",
   "Certain you display each TAI equally, and others perceived it in you?",
   "Certain each disliked TAI is equally a benefit to you as a drawback — now neither − nor +?",
   "Certain your displaying it equally served others as it cost them?",
   "Certain they showed the TAI and its exact opposite equally to the same people?",
   "Certain someone simultaneously balanced it — equal and opposite?",
   "Certain there'd be equal drawbacks had they done the opposite?",
   "Do you feel the charge has settled into gratitude / neutrality?"],
 "self_a":["Listed the specific actions you feel guilty or ashamed of?",
   "Certain others display this same TAI equally — it is shared, not uniquely yours?",
   "Certain your action was equally a benefit to them as a drawback?",
   "Certain your action was equally a benefit to you as a source of guilt? (Without flipping into pride.)",
   "Certain you showed this action and its exact opposite equally to the same person?",
   "Certain the opposite was simultaneously present to balance it?",
   "Certain there'd be equal drawbacks had you done the opposite — so nothing to feel guilty for?",
   "Do you feel the guilt has settled into self-acceptance / gratitude?"],
 "self_b":["Listed the specific actions you feel proud or arrogant about?",
   "Certain others display this same TAI equally — not uniquely yours?",
   "Certain it was equally a drawback to you as a benefit — now neither + nor −?",
   "Certain it was equally a drawback to others as a benefit?",
   "Certain you showed both pride and its exact opposite equally?",
   "Certain humility/challenge was simultaneously present to balance it?",
   "Certain there'd be equal drawbacks had you shown pure humility?",
   "Do you feel the pride has settled into humility / gratitude?"],
 "events_a":["Listed the specific distressing aspects of this situation?",
   "Certain you have produced this same outcome yourself, equally?",
   "Certain this distressing aspect is equally a benefit to you as a loss?",
   "Certain that when you produced this, it served and cost others equally?",
   "Certain the situation produced both loss and gain equally?",
   "Certain other forces simultaneously provided the opposite?",
   "Certain there'd be equal costs had it gone your way?",
   "Do you feel the distress has settled into gratitude / neutrality?"],
 "events_b":["Listed the specific aspects you're attached to or relieved by?",
   "Certain you've produced this same positive outcome before, equally?",
   "Certain this desirable aspect is equally a cost as a benefit?",
   "Certain that when you produced this, it served and cost others equally?",
   "Certain the situation produced both gain and loss equally?",
   "Certain other forces simultaneously created difficulty?",
   "Certain there'd be equal benefits had it gone badly?",
   "Do you feel the attachment has settled into gratitude / neutrality?"],
 "grief_a":["Listed specifically what you feel you have lost?",
   "Certain what you lost is now present in one or many new forms, equally?",
   "Certain the old form you mourn was equally a drawback as a benefit?",
   "Certain the new form is equally a benefit as the old — so the loss is balanced?",
   "Do you feel the grief has settled into gratitude / presence?"],
 "grief_b":["Listed specifically what you feel you have gained?",
   "Certain what you gained was already present before in another form, equally?",
   "Certain the gain is equally a cost as a benefit?",
   "Certain the old state was equally beneficial as the new — so the elation is balanced?",
   "Do you feel the elation has settled into gratitude / presence?"],
}

MODE_META={
 "others":{"title":"Dissolving Charge Toward Another Person",
   "subject_label":"Person","subject_hint":"Someone other than yourself",
   "a_label":"Side A — Infatuation (admired TAIs)",
   "b_label":"Side B — Resentment (disliked TAIs)",
   "a_desc":"Specific traits, actions or inactions in this person you most LIKE, admire, or are drawn to.",
   "b_desc":"Specific traits, actions or inactions in this person you most DISLIKE, resent, or are repelled by.",
   "ta":"Admired TAIs (Column 1)","tb":"Disliked TAIs (Column 8)",
   "ha":"e.g. 'mentors me patiently', 'speaks the truth bluntly'",
   "hb":"e.g. 'interrupts me in meetings', 'withholds praise'",
   "ca":COLS_OTHERS_A,"cb":COLS_OTHERS_B,"cia":"others_a","cib":"others_b","key":"others"},
 "self":{"title":"Dissolving Guilt / Shame & Pride / Arrogance (Your Own Conduct)",
   "subject_label":"Other Person","subject_hint":"Whom did you act toward?",
   "a_label":"Side A — Guilt & Shame (your TAIs)",
   "b_label":"Side B — Pride & Arrogance (your TAIs)",
   "a_desc":"Specific actions or inactions of YOURS toward another that you feel GUILTY or ASHAMED about.",
   "b_desc":"Specific actions or inactions of YOURS that you feel PROUD, superior, or ARROGANT about.",
   "ta":"Actions you feel guilty/ashamed of (Column 1)","tb":"Actions you feel proud/arrogant about (Column 8)",
   "ha":"e.g. 'lied about the numbers', 'walked out mid-argument'",
   "hb":"e.g. 'proved them wrong publicly', 'took sole credit'",
   "ca":COLS_SELF_A,"cb":COLS_SELF_B,"cia":"self_a","cib":"self_b","key":"self"},
 "events":{"title":"Dissolving Charge Toward an Event or Situation",
   "subject_label":"Event / Situation","subject_hint":"e.g. 'business closed', 'investment lost'",
   "a_label":"Side A — Distress & Loss",
   "b_label":"Side B — Attachment & Relief",
   "a_desc":"Specific aspects or consequences of this situation you find most NEGATIVE, threatening, or painful.",
   "b_desc":"Specific aspects or consequences you are most ATTACHED to, relieved by, or want to hold on to.",
   "ta":"Distressing aspects (Column 1)","tb":"Desirable aspects (Column 8)",
   "ha":"e.g. 'lost 3 years of savings', 'reputation damaged'",
   "hb":"e.g. 'freed from the pressure', 'unexpected cushion'",
   "ca":COLS_EVENTS_A,"cb":COLS_EVENTS_B,"cia":"events_a","cib":"events_b","key":"events"},
 "grief":{"title":"Dissolving Grief & Elation Through Change (Side C)",
   "subject_label":"Change / Loss / Gain","subject_hint":"e.g. 'father passed', 'job ended', 'windfall arrived'",
   "a_label":"Side C(loss) — Perceived LOSS / Grief",
   "b_label":"Side C(gain) — Perceived GAIN / Elation",
   "a_desc":"Specific qualities, people, capacities or states you feel you have LOST through this change.",
   "b_desc":"Specific qualities, capacities, freedoms or states you feel you have GAINED through this change.",
   "ta":"What you feel you LOST (Col C1)","tb":"What you feel you GAINED (Col C5)",
   "ha":"e.g. 'his daily phone calls', 'the team's energy'",
   "hb":"e.g. 'unexpected free time', 'new clarity of purpose'",
   "ca":COLS_GRIEF_A,"cb":COLS_GRIEF_B,"cia":"grief_a","cib":"grief_b","key":"grief"},
}

def empty_session(mode="others"):
    return {"mode":mode,"subject":"","session_date":str(date.today()),"session_note":"",
            "top_values":"","traits_a":["","",""],"traits_b":["","",""],
            "cols_a":{},"cols_b":{},"ci_a":{},"ci_b":{}}

# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Demartini Method")
        self.geometry("1120x860"); self.minsize(900,640); self.configure(bg=BG)
        try:
            p=_ico_path()
            if p: self.iconbitmap(p)
        except Exception: pass
        self._mode="others"; self._session=empty_session("others")
        self._tva=[]; self._tvb=[]; self._cta={}; self._ctb={}
        self._cia={}; self._cib={}
        self._build_chrome(); self._build_modebar(); self._build_nb()
        self.status=tk.StringVar(value=SEVEN)
        tk.Frame(self,bg=BOR,height=1).pack(fill="x",side="bottom")
        tk.Label(self,textvariable=self.status,font=("Segoe UI",8),bg=SURF,fg=TX3,
                 anchor="w").pack(fill="x",side="bottom",padx=30,pady=7)
        self._autosave_file=_autosave_path()
        self._dirty=False
        self._last_autosave=""
        self._render()
        # Offer crash recovery if an autosave from a previous session exists
        self.after(300, self._maybe_recover)
        # Begin the periodic autosave loop and save on close
        self.after(4000, self._autosave_tick)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Mark dirty whenever any field changes
        self.bind_all("<KeyRelease>", lambda e: self._mark_dirty(), add="+")

    def _build_chrome(self):
        # ── Top header bar ──────────────────────────────────────────────────
        top=tk.Frame(self,bg=SURF); top.pack(fill="x")
        inn=tk.Frame(top,bg=SURF); inn.pack(fill="x",padx=30,pady=(20,18))
        # left: title + subtitle
        title_box=tk.Frame(inn,bg=SURF); title_box.pack(side="left")
        self.title_lbl=tk.Label(title_box,text="The Demartini Method",font=FH,bg=SURF,fg=TX)
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl=tk.Label(title_box,
            text="Bringing a charged perception back into balance",
            font=FSI,bg=SURF,fg=TX3)
        self.subtitle_lbl.pack(anchor="w",pady=(3,0))
        # right: pill-style toolbar buttons with separator between groups
        bf=tk.Frame(inn,bg=SURF); bf.pack(side="right",padx=(0,2))
        # Guide (separate)
        self._tb(bf,"Guide",self.show_guide,primary=False)
        tk.Frame(bf,bg=BOR,width=1,height=20).pack(side="left",padx=10,pady=4)
        # Save / Open / Export
        self._tb(bf,"Save",self.save_session)
        self._tb(bf,"Open",self.open_session)
        self._tb(bf,"Export",self.export_txt)
        tk.Frame(bf,bg=BOR,width=1,height=20).pack(side="left",padx=10,pady=4)
        # New (destructive — slightly different look)
        self._tb(bf,"New session",self.new_session,primary=False)
        # Hairline under header
        tk.Frame(self,bg=BOR,height=1).pack(fill="x")

        # ── Meta / session info bar ─────────────────────────────────────────
        meta=tk.Frame(self,bg=SURF); meta.pack(fill="x")
        mi=tk.Frame(meta,bg=SURF); mi.pack(fill="x",padx=30,pady=(12,12))
        self.v_subj=tk.StringVar(); self.v_date=tk.StringVar(value=str(date.today()))
        self.v_note=tk.StringVar(); self.v_val=tk.StringVar()
        self._mf=self._meta(mi,"Person / Event",self.v_subj,22)
        self._meta(mi,"Date",self.v_date,11)
        self._meta(mi,"Note",self.v_note,18)
        self._meta(mi,"Your top 3 values",self.v_val,22)
        # autosave indicator (right side)
        self._as_lbl=tk.Label(mi,text="",font=FTINY,bg=SURF,fg=TX3)
        self._as_lbl.pack(side="right",padx=(0,2))
        tk.Frame(self,bg=BOR,height=1).pack(fill="x")

    def _tb(self,parent,text,cmd,primary=True):
        """Toolbar button — pill-shaped, two styles."""
        b=tk.Button(parent,text=text,command=cmd,font=FS,cursor="hand2",relief="flat",bd=0,
                    bg=SURF2 if primary else SURF,fg=TX2,
                    activebackground=BOR,activeforeground=TX,
                    padx=14,pady=6)
        b.pack(side="left",padx=2)
        return b

    def _meta(self,parent,label,var,w):
        f=tk.Frame(parent,bg=SURF); f.pack(side="left",padx=(0,24))
        tk.Label(f,text=label.upper(),font=FTINY,bg=SURF,fg=TX3).pack(anchor="w",pady=(0,4))
        e=tk.Entry(f,textvariable=var,font=FB,width=w,bg=SURF2,fg=TX,
                   relief="flat",bd=0,insertbackground=TX,
                   highlightthickness=1,highlightbackground=BOR,highlightcolor=BOR2)
        e.pack(ipady=6,ipadx=8)
        # subtle focus ring effect
        e.bind("<FocusIn>", lambda ev,en=e: en.config(highlightbackground=BOR2))
        e.bind("<FocusOut>",lambda ev,en=e: en.config(highlightbackground=BOR))
        return f

    def _build_modebar(self):
        bar=tk.Frame(self,bg=BG); bar.pack(fill="x")
        inn=tk.Frame(bar,bg=BG); inn.pack(fill="x",padx=30,pady=(14,14))
        tk.Label(inn,text="I want to process something about:",font=FTINY,
                 bg=BG,fg=TX3).pack(side="left",padx=(0,14))
        self._mbtn={}
        defs=[("others","Another person",M["others"]),
              ("self","Myself",M["self"]),
              ("events","An event",M["events"]),
              ("grief","A loss or change",M["grief"])]
        for k,lbl,colors in defs:
            b=tk.Button(inn,text=lbl,font=("Segoe UI",9),relief="flat",bd=0,
                        cursor="hand2",padx=16,pady=8,
                        command=lambda kk=k:self._switch(kk))
            b.pack(side="left",padx=(0,6))
            self._mbtn[k]=(b,colors[0],colors[1])
        self._restyle_mbtn()

    def _restyle_mbtn(self):
        for k,(b,ac,acl) in self._mbtn.items():
            if k==self._mode:
                b.config(bg=acl,fg=ac,font=("Segoe UI",9,"bold"))
            else:
                b.config(bg=SURF,fg=TX3,font=("Segoe UI",9),
                         activebackground=SURF2,activeforeground=TX)

    def _switch(self,mode):
        if mode==self._mode: return
        if not messagebox.askyesno("Switch focus",
            "Switch to a different focus?\n\nUnsaved work will be lost — save first if needed."): return
        self._mode=mode; self._session=empty_session(mode); self._restyle_mbtn(); self._render()

    def _build_nb(self):
        st=ttk.Style(self); st.theme_use("clam")
        st.configure("TNotebook",background=BG,borderwidth=0,tabmargins=[28,8,0,0])
        st.configure("TNotebook.Tab",background=BG,foreground=TX3,font=FB,
                     padding=[20,10],borderwidth=0,focuscolor=BG)
        st.map("TNotebook.Tab",
               background=[("selected",SURF)],
               foreground=[("selected",TX),("!selected",TX3)],
               expand=[("selected",[0,0,0,0])])
        st.layout("TNotebook.Tab",[("Notebook.tab",{"sticky":"nswe","children":
            [("Notebook.padding",{"side":"top","sticky":"nswe","children":
                [("Notebook.label",{"side":"top","sticky":""})]})]})])
        st.configure("TScrollbar",background=BOR2,troughcolor=SURF2,borderwidth=0,
                     arrowsize=14,gripcount=0,relief="flat")
        st.map("TScrollbar",background=[("active",TX3)])
        self.nb=ttk.Notebook(self); self.nb.pack(fill="both",expand=True)
        self._ta_out=tk.Frame(self.nb,bg=BG); self._tb_out=tk.Frame(self.nb,bg=BG)
        self.nb.add(self._ta_out,text="  Side A  "); self.nb.add(self._tb_out,text="  Side B  ")

    def _scroll(self,parent):
        cv=tk.Canvas(parent,bg=BG,bd=0,highlightthickness=0)
        sb=ttk.Scrollbar(parent,orient="vertical",command=cv.yview); cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y"); cv.pack(side="left",fill="both",expand=True)
        inner=tk.Frame(cv,bg=BG); wid=cv.create_window((0,0),window=inner,anchor="nw")
        inner.bind("<Configure>",lambda e:cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>",lambda e:cv.itemconfig(wid,width=e.width))
        cv.bind("<MouseWheel>",lambda e:cv.yview_scroll(int(-1*(e.delta/120)),"units"))
        return inner,cv

    def _render(self):
        md=MODE_META[self._mode]
        self.title_lbl.config(text="The Demartini Method")
        self._mf.winfo_children()[0].config(text=md["subject_label"].upper())
        self.nb.tab(0,text=f"  {md['a_label']}  "); self.nb.tab(1,text=f"  {md['b_label']}  ")
        for w in self._ta_out.winfo_children(): w.destroy()
        for w in self._tb_out.winfo_children(): w.destroy()
        self._inner_a,self._cv_a=self._scroll(self._ta_out)
        self._inner_b,self._cv_b=self._scroll(self._tb_out)
        self._build_side(self._inner_a,"a"); self._build_side(self._inner_b,"b")
        self._apply()

    def _build_side(self,parent,side):
        md=MODE_META[self._mode]; key=md["key"]
        ac,acl=(M[key][0],M[key][1]) if side=="a" else (M[key][2],M[key][3])
        desc=md["a_desc"] if side=="a" else md["b_desc"]

        tk.Frame(parent,bg=BG,height=16).pack()

        # ── Side description ─────────────────────────────────────────────────
        tk.Label(parent,text=desc,font=("Segoe UI",10),bg=BG,fg=TX2,
                 wraplength=860,justify="left").pack(anchor="w",padx=30,pady=(0,6))

        # ── TAI guidance banner ──────────────────────────────────────────────
        if key!="grief":
            gb=tk.Frame(parent,bg=AMBERL); gb.pack(fill="x",padx=30,pady=(0,14))
            tk.Label(gb,text="  ◆  "+TAI_GUIDE,font=FTINY,bg=AMBERL,fg=AMBER,
                     wraplength=840,justify="left").pack(anchor="w",padx=10,pady=10)

        # ── Trait / aspect list card ─────────────────────────────────────────
        col1="1" if side=="a" else "8"
        if key=="grief": col1="C1" if side=="a" else "C5"
        tc=tk.Frame(parent,bg=SURF); tc.pack(fill="x",padx=30,pady=(0,12))
        # Card header strip
        hstrip=tk.Frame(tc,bg=acl); hstrip.pack(fill="x")
        tk.Label(hstrip,text=f"  Col {col1}",font=("Segoe UI",8,"bold"),
                 bg=acl,fg=ac).pack(side="left",padx=(14,6),pady=10)
        tk.Label(hstrip,text=(md["ta"] if side=="a" else md["tb"]),
                 font=FBB,bg=acl,fg=TX).pack(side="left",pady=10)
        # Hint
        tk.Label(tc,text=(md["ha"] if side=="a" else md["hb"]),
                 font=FSI,bg=SURF,fg=TX3,wraplength=820,justify="left").pack(anchor="w",padx=16,pady=(10,2))
        tk.Label(tc,text="Start with your top three. You can add more if needed.",
                 font=("Segoe UI",8),bg=SURF,fg=TX3).pack(anchor="w",padx=16,pady=(0,8))
        # Trait entries
        tf=tk.Frame(tc,bg=SURF); tf.pack(fill="x",padx=16,pady=(0,4))
        vars_list=[]
        if side=="a": self._tva=vars_list; self._tfa=tf
        else: self._tvb=vars_list; self._tfb=tf
        for t in self._session.get(f"traits_{side}",["","",""]):
            vars_list.append(tk.StringVar(value=t))
        self._render_traits(tf,vars_list,side,ac)
        # Add button
        ab=tk.Button(tc,text="＋  Add another",font=("Segoe UI",9),bg=SURF,fg=ac,
                     relief="flat",bd=0,cursor="hand2",activebackground=acl,
                     activeforeground=ac,padx=6,pady=4,
                     command=lambda s=side,vl=vars_list,t=tf,a=ac:self._add_trait(s,vl,t,a))
        ab.pack(anchor="w",padx=16,pady=(2,14))

        # ── Column cards ─────────────────────────────────────────────────────
        col_defs=md["ca"] if side=="a" else md["cb"]
        col_texts={}
        if side=="a": self._cta=col_texts
        else: self._ctb=col_texts
        for cid,title,prompt,q in col_defs:
            card=tk.Frame(parent,bg=SURF); card.pack(fill="x",padx=30,pady=(0,10))
            # Header strip with col badge + title
            hstrip=tk.Frame(card,bg=acl); hstrip.pack(fill="x")
            tk.Label(hstrip,text=f"  Col {cid}",font=("Segoe UI",8,"bold"),
                     bg=acl,fg=ac).pack(side="left",padx=(14,8),pady=9)
            tk.Label(hstrip,text=title,font=FBB,bg=acl,fg=TX).pack(side="left",pady=9)
            # Prompt
            tk.Label(card,text=prompt,font=("Segoe UI",9),bg=SURF,fg=TX2,
                     justify="left",anchor="w",wraplength=830).pack(anchor="w",padx=18,pady=(10,4))
            # Answer boxes
            bf=tk.Frame(card,bg=SURF); bf.pack(fill="x",padx=18,pady=(4,4))
            tlist=[]; col_texts[cid]=tlist
            saved=self._session.get(f"cols_{side}",{}).get(cid,[])
            for i in range(len(vars_list)):
                self._add_box(bf,tlist,vars_list,i,saved[i] if i<len(saved) else "",ac,acl)
            card._bf=bf; card._cid=cid; card._side=side
            # Equilibration question — pill at the bottom
            qf=tk.Frame(card,bg=SURF); qf.pack(fill="x",padx=18,pady=(6,14))
            qpill=tk.Frame(qf,bg=acl); qpill.pack(anchor="w")
            tk.Label(qpill,text="✓  "+q,font=("Segoe UI",8,"italic"),
                     bg=acl,fg=ac,justify="left",wraplength=800).pack(anchor="w",padx=12,pady=7)

        if side=="a":
            self._cards_a=[w for w in parent.winfo_children()
                           if isinstance(w,tk.Frame) and hasattr(w,"_cid")]
        else:
            self._cards_b=[w for w in parent.winfo_children()
                           if isinstance(w,tk.Frame) and hasattr(w,"_cid")]

        # ── Equilibration check-in ───────────────────────────────────────────
        cik=md["cia"] if side=="a" else md["cib"]; qs=CHECKINS[cik]
        civ={}
        if side=="a": self._cia=civ
        else: self._cib=civ
        cic=tk.Frame(parent,bg=SURF); cic.pack(fill="x",padx=30,pady=(4,4))
        # Check-in header
        chstrip=tk.Frame(cic,bg=GRL); chstrip.pack(fill="x")
        tk.Label(chstrip,text="  ✓  Equilibration check-in",font=("Segoe UI",10,"bold"),
                 bg=GRL,fg=GR).pack(side="left",padx=14,pady=12)
        tk.Label(chstrip,text="Mark each Yes when you genuinely feel the balance",
                 font=FTINY,bg=GRL,fg=GR).pack(side="left")
        # Questions
        saved_ci=self._session.get(f"ci_{side}",{})
        for i,q in enumerate(qs):
            is_last=(i==len(qs)-1)
            row=tk.Frame(cic,bg=SURF if i%2==0 else SURF2)
            row.pack(fill="x")
            tk.Label(row,text=f"  {i+1}",font=("Segoe UI",8),
                     bg=row["bg"],fg=TX3,width=3,anchor="e").pack(side="left",pady=10)
            tk.Label(row,text=q,font=("Segoe UI",9),bg=row["bg"],fg=TX2,
                     anchor="w",justify="left",wraplength=640).pack(side="left",fill="x",
                     expand=True,padx=(8,12),pady=10)
            sv=tk.StringVar(value=saved_ci.get(str(i),"")); civ[i]=sv
            nbg=row["bg"]
            yb=tk.Button(row,text="  Yes  ",font=("Segoe UI",8),relief="flat",bd=0,
                         cursor="hand2",bg=nbg,fg=TX3,padx=4,pady=4)
            nb=tk.Button(row,text="Not yet",font=("Segoe UI",8),relief="flat",bd=0,
                         cursor="hand2",bg=nbg,fg=TX3,padx=4,pady=4)
            def _set(val,yb=yb,nb=nb,sv=sv):
                sv.set(val)
                yb.config(bg=GRL,fg=GR,font=("Segoe UI",8,"bold")) if val=="yes" else yb.config(bg=nbg,fg=TX3,font=("Segoe UI",8))
                nb.config(bg=M[key][3],fg=M[key][2]) if val=="no" else nb.config(bg=nbg,fg=TX3)
            yb.config(command=lambda s=_set:s("yes")); nb.config(command=lambda s=_set:s("no"))
            if sv.get(): _set(sv.get(),yb,nb,sv)
            nb.pack(side="right",padx=(4,14)); yb.pack(side="right",padx=4)
            if not is_last:
                tk.Frame(cic,bg=BOR,height=1).pack(fill="x")

        # ── Completion note ──────────────────────────────────────────────────
        tk.Frame(parent,bg=BG,height=10).pack()
        cn=tk.Frame(parent,bg=GRL); cn.pack(fill="x",padx=30)
        tk.Label(cn,
            text="◆   Completion is felt, not forced. The charge dissolves into genuine gratitude — "
                 "a quiet settling, moist eyes, a soft 'thank you'. "
                 "If a pull remains, there are more answers to gather. "
                 "Balance, not suppression, is the destination.",
            font=("Segoe UI",9,"italic"),bg=GRL,fg=GRD,
            wraplength=820,justify="left").pack(anchor="w",padx=18,pady=14)
        tk.Frame(parent,height=48,bg=BG).pack()

    def _render_traits(self,frame,vars_list,side,ac):
        for w in frame.winfo_children(): w.destroy()
        for i,v in enumerate(vars_list):
            row=tk.Frame(frame,bg=SURF)
            row.grid(row=i//2,column=i%2,sticky="ew",padx=(0,12),pady=4)
            frame.columnconfigure(0,weight=1); frame.columnconfigure(1,weight=1)
            # Number badge
            num=tk.Label(row,text=str(i+1),font=("Segoe UI",8,"bold"),
                         bg=SURF2,fg=TX3,width=2,anchor="center")
            num.pack(side="left",padx=(0,6),ipady=3,ipadx=2)
            # Entry
            e=tk.Entry(row,textvariable=v,font=("Segoe UI",10),bg=SURF2,fg=TX,
                       relief="flat",bd=0,insertbackground=TX,
                       highlightthickness=1,highlightbackground=BOR,highlightcolor=ac)
            e.pack(side="left",fill="x",expand=True,ipady=7,ipadx=8)
            e.bind("<FocusIn>", lambda ev,en=e:en.config(highlightbackground=ac,bg=SURF))
            e.bind("<FocusOut>",lambda ev,en=e:en.config(highlightbackground=BOR,bg=SURF2))
            # Remove button (only when >1 trait)
            if len(vars_list)>1:
                tk.Button(row,text="−",font=("Segoe UI",11),bg=SURF,fg=TX3,
                          relief="flat",bd=0,cursor="hand2",padx=8,pady=0,
                          activebackground=SURF2,activeforeground=TX2,
                          command=lambda idx=i,s=side:self._remove_trait(idx,s)).pack(side="left",padx=(4,0))

    def _add_trait(self,side,vars_list,frame,ac):
        vars_list.append(tk.StringVar()); self._render_traits(frame,vars_list,side,ac)
        col_texts=self._cta if side=="a" else self._ctb
        cards=self._cards_a if side=="a" else self._cards_b
        key=MODE_META[self._mode]["key"]
        acl=M[key][1] if side=="a" else M[key][3]
        for card in cards:
            self._add_box(card._bf,col_texts[card._cid],vars_list,len(vars_list)-1,"",ac,acl)
        (self._cv_a if side=="a" else self._cv_b).after(80,lambda:(self._cv_a if side=="a" else self._cv_b).yview_moveto(1.0))

    def _remove_trait(self,idx,side):
        vars_list=self._tva if side=="a" else self._tvb
        frame=self._tfa if side=="a" else self._tfb
        key=MODE_META[self._mode]["key"]
        ac,acl=(M[key][0],M[key][1]) if side=="a" else (M[key][2],M[key][3])
        col_texts=self._cta if side=="a" else self._ctb
        cards=self._cards_a if side=="a" else self._cards_b
        if len(vars_list)<=1: return
        vars_list.pop(idx); self._render_traits(frame,vars_list,side,ac)
        for cid,tlist in col_texts.items():
            if idx<len(tlist): tlist.pop(idx)
        for card in cards:
            tlist=col_texts[card._cid]
            saved=[t.get("1.0","end-1c") for t in tlist]
            for w in card._bf.winfo_children(): w.destroy()
            tlist.clear()
            for i,c in enumerate(saved): self._add_box(card._bf,tlist,vars_list,i,c,ac,acl)

    def _add_box(self,frame,tlist,vars_list,idx,content,ac,acl):
        outer=tk.Frame(frame,bg=SURF); outer.pack(fill="x",pady=(0,12))
        # Live label showing which trait this box is for
        def mk():
            v=vars_list[idx] if idx<len(vars_list) else None
            t=v.get().strip() if v else ""
            return f"  {idx+1}.  {t if t else f'Trait {idx+1}'}"
        lbl_row=tk.Frame(outer,bg=acl); lbl_row.pack(fill="x")
        lbl=tk.Label(lbl_row,text=mk(),font=("Segoe UI",8,"italic"),
                     bg=acl,fg=ac,anchor="w")
        lbl.pack(side="left",padx=4,pady=5)
        if idx<len(vars_list):
            def _upd(*_a,l=lbl,f=mk):
                try:
                    if l.winfo_exists(): l.config(text=f())
                except tk.TclError: pass
            vars_list[idx].trace_add("write",_upd)
        # Text area
        txt=tk.Text(outer,font=("Segoe UI",10),bg=SURF2,fg=TX,relief="flat",bd=0,
                    wrap="word",height=5,insertbackground=TX,
                    selectbackground=acl,
                    highlightthickness=1,highlightbackground=BOR,highlightcolor=ac,
                    spacing1=2,spacing3=4,padx=12,pady=10)
        txt.pack(fill="x")
        if content: txt.insert("1.0",content)
        # Focus glow
        txt.bind("<FocusIn>", lambda e,t=txt:t.config(highlightbackground=ac,bg=SURF))
        txt.bind("<FocusOut>",lambda e,t=txt:t.config(highlightbackground=BOR,bg=SURF2))
        sb=ttk.Scrollbar(outer,command=txt.yview); txt.configure(yscrollcommand=sb.set)
        txt.bind("<FocusIn>", lambda e,s=sb,t=txt:(s.pack(side="right",fill="y"),
                                                    t.config(highlightbackground=ac,bg=SURF)))
        txt.bind("<FocusOut>",lambda e,s=sb,t=txt:(s.pack_forget(),
                                                    t.config(highlightbackground=BOR,bg=SURF2)))
        tlist.append(txt)

    def _apply(self):
        s=self._session
        self.v_subj.set(s.get("subject","")); self.v_date.set(s.get("session_date",str(date.today())))
        self.v_note.set(s.get("session_note","")); self.v_val.set(s.get("top_values",""))

    def _gather(self):
        def td(ct): return {cid:[t.get("1.0","end-1c") for t in lst] for cid,lst in ct.items()}
        return {"mode":self._mode,"subject":self.v_subj.get(),"session_date":self.v_date.get(),
                "session_note":self.v_note.get(),"top_values":self.v_val.get(),
                "traits_a":[v.get() for v in self._tva],"traits_b":[v.get() for v in self._tvb],
                "cols_a":td(self._cta),"cols_b":td(self._ctb),
                "ci_a":{str(k):v.get() for k,v in self._cia.items()},
                "ci_b":{str(k):v.get() for k,v in self._cib.items()}}

    # ── autosave & crash recovery ─────────────────────────────────────────────
    def _mark_dirty(self,*_):
        self._dirty=True

    def _has_content(self,d):
        """True if the session holds anything worth recovering."""
        if d.get("subject") or d.get("session_note") or d.get("top_values"): return True
        if any(t.strip() for t in d.get("traits_a",[])): return True
        if any(t.strip() for t in d.get("traits_b",[])): return True
        for side in ("cols_a","cols_b"):
            for boxes in d.get(side,{}).values():
                if any(b.strip() for b in boxes): return True
        if any(v for v in d.get("ci_a",{}).values()): return True
        if any(v for v in d.get("ci_b",{}).values()): return True
        return False

    def _write_autosave(self):
        try:
            d=self._gather()
            if not self._has_content(d):
                return
            payload=json.dumps(d,ensure_ascii=False)
            if payload==self._last_autosave:
                return  # nothing changed since last write
            tmp=self._autosave_file+".tmp"
            with open(tmp,"w",encoding="utf-8") as f:
                f.write(payload)
            os.replace(tmp,self._autosave_file)  # atomic — survives mid-write crash
            self._last_autosave=payload
            # Show subtle "saved" tick in meta bar for 2 seconds
            try:
                self._as_lbl.config(text="  ✓ saved",fg=GR)
                self.after(2000,lambda:self._as_lbl.config(text="",fg=TX3))
            except Exception: pass
        except Exception:
            pass  # never let autosave interrupt the user

    def _autosave_tick(self):
        # Snapshot every few seconds; cheap because it skips when unchanged
        if not self.winfo_exists():
            return
        self._write_autosave()
        self.after(4000, self._autosave_tick)

    def _maybe_recover(self):
        try:
            if not os.path.exists(self._autosave_file):
                return
            d=json.load(open(self._autosave_file,encoding="utf-8"))
            if not self._has_content(d):
                return
            when=""
            try:
                import time
                mt=os.path.getmtime(self._autosave_file)
                when=" from "+time.strftime("%d %b %Y, %H:%M",time.localtime(mt))
            except Exception: pass
            if messagebox.askyesno("Recover unsaved work",
                f"An auto-saved session was found{when}.\n\n"
                "This usually means the app closed unexpectedly last time.\n\n"
                "Restore it now?"):
                m=d.get("mode","others")
                if m!=self._mode: self._mode=m; self._restyle_mbtn()
                self._session=d; self._render()
                self.status.set("Recovered auto-saved session")
                self._last_autosave=json.dumps(d,ensure_ascii=False)
            else:
                # User declined — clear it so they aren't asked again
                self._clear_autosave()
        except Exception:
            pass

    def _clear_autosave(self):
        try:
            if os.path.exists(self._autosave_file):
                os.remove(self._autosave_file)
        except Exception: pass
        self._last_autosave=""

    def _on_close(self):
        # Final autosave on graceful close, then exit
        self._write_autosave()
        self.destroy()

    def save_session(self):
        d=self._gather(); subj=(d["subject"] or "session").replace(" ","_")[:25]
        p=filedialog.asksaveasfilename(title="Save",defaultextension=".json",
            initialfile=f"demartini-{d['mode']}-{subj}-{d['session_date']}.json",
            filetypes=[("Session","*.json"),("All","*.*")])
        if not p: return
        with open(p,"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)
        self._clear_autosave()
        self.status.set(f"Saved → {os.path.basename(p)}")

    def open_session(self):
        p=filedialog.askopenfilename(title="Open",filetypes=[("Session","*.json"),("All","*.*")])
        if not p: return
        try:
            d=json.load(open(p,encoding="utf-8"))
            m=d.get("mode","others")
            if m!=self._mode: self._mode=m; self._restyle_mbtn()
            self._session=d; self._render(); self.status.set(f"Loaded ← {os.path.basename(p)}")
            self._last_autosave=""  # next tick will autosave the loaded session afresh
        except Exception as e: messagebox.showerror("Error",f"Could not load:\n{e}")

    def new_session(self):
        if not messagebox.askyesno("New","Clear everything?"): return
        self._clear_autosave()
        self._session=empty_session(self._mode); self._render(); self.status.set("New session")

    def export_txt(self):
        d=self._gather(); md=MODE_META[self._mode]; subj=(d["subject"] or "session").replace(" ","_")[:25]
        p=filedialog.asksaveasfilename(title="Export",defaultextension=".txt",
            initialfile=f"demartini-{d['mode']}-{subj}-{d['session_date']}.txt",
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not p: return
        def ci(c,i): return "[YES]" if c.get(str(i))=="yes" else "[  ]"
        L=["="*72,f"  THE DEMARTINI METHOD — {md['title']}","="*72,
           f"  Subject    : {d.get('subject','-')}",f"  Date       : {d.get('session_date','-')}",
           f"  Note       : {d.get('session_note','-')}",f"  Top Values : {d.get('top_values','-')}","",SEVEN,""]
        for side in ("a","b"):
            lbl=md["a_label"] if side=="a" else md["b_label"]
            L+=["─"*72,f"  {lbl}","─"*72,""]
            traits=d.get(f"traits_{side}",[])
            L.append("Items:")
            for i,t in enumerate(traits): L.append(f"  {i+1}. {t}")
            L.append("")
            cdefs=md["ca"] if side=="a" else md["cb"]; cdata=d.get(f"cols_{side}",{})
            for cid,title,_,_ in cdefs:
                L.append(f"Col {cid} — {title}:")
                for i,(t,c) in enumerate(zip(traits,cdata.get(cid,[]))):
                    L.append(f"  [{i+1}. {t}]"); L.append(f"  {c or '(empty)'}"); L.append("")
            cik=md["cia"] if side=="a" else md["cib"]
            L.append(f"Equilibration check-in:")
            for i,q in enumerate(CHECKINS[cik]): L.append(f"  {ci(d.get(f'ci_{side}',{}),i)} {q}")
            L.append("")
        L.append("="*72)
        open(p,"w",encoding="utf-8").write("\n".join(L))
        self.status.set(f"Exported → {os.path.basename(p)}")

    def show_guide(self):
        g=tk.Toplevel(self); g.title("How to use this method"); g.geometry("640x680"); g.configure(bg=BG)
        try:
            pth=_ico_path()
            if pth: g.iconbitmap(pth)
        except Exception: pass
        txt=tk.Text(g,font=FB,bg=SURF,fg=TX,relief="flat",wrap="word",padx=20,pady=18,spacing3=4)
        txt.pack(fill="both",expand=True,padx=12,pady=12)
        guide="""THE DEMARTINI METHOD — A Quick Facilitation Guide

PURPOSE
Every emotion is a ratio of perceptions. When you perceive more upside than downside you become infatuated (or proud); more downside than upside, resentful (or guilty/grieving). The Method gathers the missing side until the perception is balanced — and a balanced perception releases the charge into gratitude and presence.

CHOOSE YOUR MODE
• Others — a charge toward another person (resentment OR infatuation).
• Self — a charge toward your OWN conduct (guilt/shame OR pride/arrogance).
• Events — a charge toward a situation with no single human cause.
• Grief / Change — a perceived loss OR gain through a change (Side C).

STEP 1 — IDENTIFY THE TAI
List the top 3 highest-priority Traits, Actions or Inactions (Col 1 / 8). Be surgical: a TAI is observable in 3–4 words. Exclude feelings (loving, humiliated), synonyms (nice, mean) and labels (good person, abusive). Pinpoint where, when, and to whom.

STEP 2 — WORK EACH COLUMN, PER ITEM
Each column has one box per item you listed. Answer fully for each before moving on. Quantity matters: keep adding real, specific moments until the two sides truly equalise. Use the Seven Areas and move through time (past → present).

STEP 3 — THE BALANCING LOGIC
• Reflection: you (or others) own the same TAI equally.
• Drawbacks/Benefits: the charged trait carries the opposite value too.
• Opposite to the same person: dissolves 'always / never' labels.
• Synchronicity: someone provided the exact opposite at that very moment.
• Antidote: had it gone the other way, the consequences would equalise.

STEP 4 — EQUILIBRATE
Use the check-in questions. The aim is "neither positive nor negative." If a question still gets a "not yet," return to that column and gather more.

STEP 5 — COMPLETION
Completion is felt, not forced: genuine gratitude, often moist eyes and a settled body. Don't suppress the feeling — balance it. When both sides are equal, the love and presence underneath naturally surface.

A note on the Self mode: in Column 4, check every three answers so dissolving guilt does not over-shoot into pride. The destination is equilibrium, not a new charge.

AUTOSAVE & RECOVERY
Your work is auto-saved every few seconds in the background. If the app or your computer closes unexpectedly, you'll be offered the chance to restore it the next time you open the app. For a permanent copy you can name and keep, still use Save (and Export for a readable text version).

This app is a faithful working tool, not a substitute for a trained facilitator or professional care where that is needed."""
        txt.insert("1.0",guide); txt.config(state="disabled")
        tk.Button(g,text="Close",command=g.destroy,font=FS,bg=SURF2,fg=TX2,relief="flat",
                  cursor="hand2",padx=16,pady=6,bd=0).pack(pady=(0,14))

if __name__=="__main__":
    _f=os.path.join(os.path.dirname(__file__),"demartini.ico")
    if os.path.exists(_f):
        _ICO=base64.b64encode(open(_f,"rb").read()).decode("ascii")
    App().mainloop()
