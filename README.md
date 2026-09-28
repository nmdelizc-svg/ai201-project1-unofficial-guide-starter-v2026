# The Unofficial Guide

Nancy Deliz Camacho - Using Advice_threads

# Unit 1

## What This Does

I picked the `advice_threads` corpus: 23 threads of student advice, each one a
question with a handful of upvoted replies under it. It's the kind of thing you
get pointed at when you ask an older student something and they say "this came
up last year." The system searches those threads and answers questions about
campus life in a few sentences, naming the thread it got the answer from — how
much time a bike actually saves over walking, what month to start applying for
summer internships, whether it's weird to turn up to office hours without a
specific question, how much RAM a CS laptop needs. If you ask it something the
threads don't cover, it says it doesn't have enough information rather than
guessing.

## Chunking Strategy

**Chunk size:** 800 characters — kept from the starter
**Overlap:** none (replaced by a repeated THREAD line)

**What the starter did.** Its summary line read `26 chunks, 487 characters on
average (shortest 2, longest 793)`. I assumed at first that the three extra
chunks were documents too long for the window. They weren't — nothing in my
corpus reaches 800 characters. They came from the **stride**. `fallback_split`
advances `chunk_size - overlap` = 680 characters, so every document between 681
and 800 characters gets a second window holding only its tail:

| Document | Length | Tail chunk it produced |
|---|---|---|
| thread_first_year_regret.txt | 793 | 113 chars, starting `) ---` |
| thread_bike_commute.txt | 739 | 59 chars, `nd it's the only reason I got mine back…` |
| thread_meal_plan_tier.txt | 682 | 2 chars, `t.` |

793 − 680 = 113, 739 − 680 = 59, 682 − 680 = 2. The overlap — the thing that
exists so a thought isn't lost at a boundary — is precisely what manufactured
three fragments with no thought in them at all. That also explains why the
three chunks cut mid-sentence were the same three shorter than 200 characters,
which I'd noticed in criteria.md without knowing the cause.

**The decision.** One thread stays one chunk. A thread is a question with its
answers underneath it, a reply that loses its question is close to useless, and
all 23 of my documents already fit inside the window (average 543, longest
793). So there is no reason to cut any of them.

**The numbers.** 800 characters, unchanged — it sits above my longest document,
so on this corpus it's a ceiling for growth rather than a knife. Overlap goes
to zero: it caused all of the damage, and the context it was meant to preserve
I handle instead by repeating the `THREAD:` line at the top of every piece if a
thread ever does have to come apart. When one does, it splits between replies
on the `--- reply N (X votes) ---` markers the documents already carry, never
inside one. Only a single reply longer than 800 characters falls back to a
sentence split, and nothing in this corpus triggers it.

**Result.** `23 chunks, 543 characters on average (shortest 317, longest 793),
produced by chunker.py::split_documents`. 26 → 23, shortest 2 → 317. One
document, one chunk, and criterion 4 holds by construction rather than by luck.

## Sample Chunks

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_professor_email.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Do professors actually answer email?

--- reply 1 (21 votes) ---
Varies enormously. General rule I've found: if the syllabus states a response window, it's honoured. If it doesn't, assume 48 hours and don't panic before then.

--- reply 2 (33 votes) ---
Office hours are dramatically more effective than email for anything that takes more than two sentences to answer. They're also usually empty.

--- reply 3 (15 votes) ---
Empty office hours is the biggest unused resource here and I say that having wasted a year not going.
```

All five are whole threads, which is the point of the strategy above: a chunk
is a question with its answers attached, so any one of them can be read on its
own. Under the starter's chunker the first of these five also produced a
59-character tail (`nd it's the only reason I got mine back…`); it doesn't
exist any more.

## Sample Answer

**Question:** Is it weird to go to office hours without a specific question?

**Answer:**

```
  (best distance 0.390, cutoff 0.6)

No, it is not weird, and it is considered a completely normal thing to say you
are following the lectures but do not feel like you understand the shape of the
material.

Source: `thread_office_hours_etiquette.txt`

Sources retrieved: thread_office_hours_etiquette.txt, thread_professor_email.txt, thread_study_spots.txt

1 model calls this session, 636 tokens (585 in, 51 out)
```

Produced by `python app.py ask "..."` — `generate.py::answer_from_chunks`. Note
the gap between the two source lines: three chunks were retrieved and handed to
the model, and the model named the one it actually used. That distinction is
what criterion 2 in criteria.md is scoring.

**My relevance cutoff:**

**0.6**, set in `config.py`. Measured with `python app.py retrieve` on all ten
questions, which costs no model calls.

| Question | In corpus? | Best distance |
|---|---|---|
| How much RAM do I need for a CS laptop? | Yes | 0.2869 |
| For summer internships, around what month should I start applying? | Yes | 0.3287 |
| When do small local employers hire summer interns? | Yes | 0.3418 |
| Is it weird to go to office hours without a specific question? | Yes | 0.3898 |
| How long is the bike ride to campus? | Yes | 0.4206 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8280 |
| How do I write a for loop in Rust? | No | 0.8712 |
| How do I change the oil in a diesel engine? | No | 0.9299 |
| What is the capital of Mongolia? | No | 0.9479 |
| Who won the 1994 World Cup? | No | 0.9517 |

The two groups don't overlap and it isn't close. In-corpus runs 0.2869–0.4206,
out-of-corpus runs 0.8280–0.9517, and the 0.4074 between them is empty. The
midpoint of that gap is 0.6243, so the 0.6 the starter ships with is almost
exactly where I'd have put it anyway. Anywhere from about 0.45 to 0.8 sorts
these ten identically; I'm keeping 0.6 because it sits in open space rather
than near either edge.

**The chunker moved this.** These aren't the numbers I measured before
Milestone 3. The in-corpus five are unchanged to four decimal places, because
none of those threads was ever split. Every out-of-corpus distance went **up**:

| Out-of-corpus question | Before | After | Nearest chunk before |
|---|---|---|---|
| Who won the 1994 World Cup? | 0.7866 | 0.9517 | `t.` (2 chars) |
| What is the capital of Mongolia? | 0.8902 | 0.9479 | `nd it's the only reason…` |

The junk fragments were the nearest neighbours for nonsense questions — a
2-character chunk carries no meaning, so it sits a middling distance from
everything, including things my corpus has nothing to say about. Deleting them
raised the out-of-corpus floor from 0.7866 to 0.8280 and widened the gap from
0.3660 to 0.4074. Fixing chunking bought the gate margin it never had.

The closest call on either side is the bike question at 0.4206, and it's
instructive: the thread is titled "Is a bike worth it for a 20 minute walk
commute?" and my question asks how long the ride is. The answer is in there
("cuts an 18 minute walk to about 6") but the wording barely overlaps, which
is why it scores furthest from the corpus of the five. Still 0.18 clear of the
cutoff.

**My top-k:** **3**, down from the starter's 5. I read the chunks that came
back for three questions and the tail was dead weight. Distance by rank across
all five in-corpus questions:

| Question | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| How much RAM do I need for a CS laptop? | 0.2869 | 0.8689 | 0.8767 | 0.8794 | 0.8986 |
| For summer internships, what month? | 0.3287 | 0.7452 | 0.7949 | 0.7983 | 0.8097 |
| When do small local employers hire? | 0.3418 | 0.7283 | 0.7775 | 0.7948 | 0.7956 |
| Is it weird to go to office hours? | 0.3898 | 0.5881 | 0.7386 | 0.7455 | 0.7478 |
| How long is the bike ride to campus? | 0.4206 | 0.5170 | 0.7468 | 0.7625 | 0.7632 |

Rank 1 is the right thread every time. Rank 2 is genuinely useful twice — the
office-hours question pulls `thread_professor_email.txt` at 0.5881 and the bike
question pulls `thread_commuting.txt` at 0.5170, both real second opinions and
both under my cutoff. **Rank 3 never once drops below 0.7386**, which puts the
whole tail in the same distance band as the out-of-corpus questions the gate
exists to refuse. Handing the model three threads it would refuse on their own
is how answers drift. Strictly the data supports top-k of 2; I set 3 to leave
one slot for a question whose answer legitimately spans three threads, and the
cost of being wrong is one off-topic chunk rather than three. Concretely it
took the office-hours prompt from 773 input tokens to 585.

**The grounding instruction:** I read `GROUNDING_INSTRUCTION` with
`python app.py ask "..." --show-prompt`. Three of its four rules were already
right for my corpus. The gap was that it treats each excerpt as a document that
simply states things, and mine don't — mine are threads where the replies argue
with each other. `thread_bike_commute.txt` has reply 1 saying a bike is worth
it and reply 2 saying "Counterpoint, I sold mine", and nothing in the
instruction stopped the model from picking a side and reporting it as settled.
I added two rules: say so when the replies disagree and give both positions,
and don't add advice that isn't in the documents however sensible it sounds.
The second is aimed at the failure mode the brief describes — an answer that
sounds right, cites nothing, and came from training data.

## How I Used AI

I used AI mainly to check my own reasoning rather than to write things for me.
Once I have an explanation in my head I tend to stop looking, and both of the
moments below are cases where I'd settled on something and was wrong about it.

**1. Checking a diagnosis I'd already committed to.** I'd written in
`criteria.md` that my three broken chunks came from the 800-character window
"closing wherever it happens to land" in the middle of a sentence. It was a
tidy story and I stopped there. I asked Claude to check it against the actual
numbers before I replaced the chunker. It came back with something I hadn't
considered: **no document in my corpus reaches 800 characters at all**, so the
window never fired. The fragments came from the stride — `fallback_split`
advances `chunk_size - overlap` = 680, so any document between 681 and 800
characters gets a second window holding only its tail. 793 − 680 = 113,
739 − 680 = 59, 682 − 680 = 2. That last one is the `t.` chunk. The overlap,
which is supposed to stop a thought being lost at a boundary, was the thing
creating fragments with no thought in them.

What I changed: the chunker I'd planned was a reply-boundary splitter, and I
kept that, but the reason changed completely. I'd been about to set overlap to
something smaller. Knowing the stride was the cause, I set it to **zero** and
handled the context it was protecting by repeating the `THREAD:` line on every
piece instead. I also rewrote the Chunking Strategy section above, because what
I'd written there was a plausible explanation of the wrong mechanism.

**2. Checking my criteria for gaps in the logic.** I asked Claude to read
`criteria.md` against the rubric and say whether each criterion was clear and
well-argued. Criterion 1 was the useful catch: my reasoning argued that TOP_K
of 5 against a small corpus made the bar easy, and then kept the loose "4 of 5"
target anyway — I'd written an argument for tightening and used it as a defence
of not tightening, and I genuinely hadn't seen that reading. It also noticed
that criterion 5 opened with "my system can refuse in two different places" and
then only ever described one of them.

What I changed: I kept both targets where they were rather than moving a number
to match the argument. Criterion 1 now names the single question I actually
expect to fail instead of hand-waving at the odds, and criterion 5 describes
the second refusal site — the model's own judgement, which is the one I don't
control. I didn't take every suggestion: it wanted me to resolve the tension
between criteria 1 and 5 by adjusting a target, and I'd rather leave both alone
and say plainly that if they fail, they'll fail together for one reason.

The same habit caught a smaller thing worth recording: `config.py` had `CORPUS`
defaulting to `campus_life`, and my actual choice of `advice_threads` lived
only in `.env`, which is gitignored. Anyone cloning this repo would have
indexed 88 documents instead of my 23 and none of my numbers would have
reproduced. I changed the default so the corpus choice is committed.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. No chunk is cut mid-sentence | 0 of 23 |  |  |  |  |
| 5. No in-scope question comes back refused | 0 of 5 |  |  |  |  |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. No chunk is cut mid-sentence | 0 of 23 |  |  |  |  |
| 5. No in-scope question comes back refused | 0 of 5 |  |  |  |  |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
