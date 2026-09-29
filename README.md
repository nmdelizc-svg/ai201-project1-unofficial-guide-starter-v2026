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
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk is cut mid-sentence | 0 of 23 | 0 of 23 | 0 of 23 | 0 of 23 | MET |
| 5. No in-scope question comes back refused | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | MET |

Source run: `results/run_2026-09-28_1429_before.md`, written by
`run_eval.py::main` on 2026-09-28 — corpus `advice_threads`, top-k 3,
cutoff 0.6, three runs per question, caching off. That file is one row per
question; this table is one row per criterion, so the counts below are that
file aggregated.

Two rows are measured in one pass rather than three, and the same number goes
in all three columns. Criterion 3 is deterministic: retrieval doesn't vary and
the gate is a comparison against a fixed number, so one pass over the
out-of-scope list is the whole measurement. Criterion 4 isn't produced by
`run_eval.py` at all — it's a property of the index, not of a question, so it
comes from `chunker.py::split_documents` and is checked across all 23 chunks.

### Real output

**Criterion 1 — retrieved chunks contain the answer.** Scored off the
`Sources retrieved` line, which `run_eval.py::main` prints from
`store.py::search` before generation. Run 1, the question I'd predicted would
be the one to miss:

```
### When do small local employers hire summer interns? — run 1

- Best distance: 0.3418 (passed the gate)
- Sources retrieved: thread_first_gen.txt, thread_internship_timing.txt, thread_laundry_timing.txt
```

`thread_internship_timing.txt` is the thread holding the answer, and it came
back at rank 1 in all three runs. Same for the other four questions.

**Criterion 2 — every answer names a source.** Produced by
`generate.py::answer_from_chunks`. All 15 answers name a file; the model picks
its own format, which is why these three are the same claim written three ways:

```
According to *thread_laptop_specs.txt*, 16GB of RAM is recommended as the number worth paying for. One reply notes that 8GB can work for a couple of years, but struggled by the final project.
```

```
Small and local places hire summer interns in February and March (*thread_internship_timing.txt*).
```

```
No, it is not weird to go to office hours without a specific question; one commenter states that saying you are following the lectures but do not understand the shape of it is completely normal. 

Source: `thread_office_hours_etiquette.txt`
```

**Criterion 3 — the gate stops out-of-corpus questions.** Produced by
`run_eval.py::check_out_of_scope` against `gate.py`. Refused 5 of 5:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.948 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.952 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |

What a refusal actually looks like, from `python app.py ask "Who won the 1994
World Cup?"`:

```
  (best distance 0.952, cutoff 0.6)

I don't have enough information about that.

0 model calls this session
```

The last line is the part worth noting: the gate refuses before the model is
called, so an out-of-corpus question costs nothing.

**Criterion 4 — no chunk is cut mid-sentence.** Measured over the whole index
rather than a sample, by calling `chunker.py::split_documents` directly:

```
total chunks: 23
not starting at a thread header: 0
not ending on sentence-final punctuation: 0
shortest: 317 longest: 793
```

The shortest chunk is 317 characters. The three failures I wrote this criterion
about — `t.`, `nd it's the only reason…` and `) ---` — are gone, because the
reply-boundary splitter can't produce them.

**Criterion 5 — no in-scope question comes back refused.** Scored by searching
all 15 answers for the phrase "don't have enough information". Zero hits. Every
in-scope question cleared the gate with room: the closest was the bike question
at 0.4206 against a cutoff of 0.6.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | 5 of 5 against a target of 4 of 5, and the same 5 in all three runs. Not close, and not close in the direction I expected — see below. |
| 2 | Every answer names a source | MET | 15 of 15 answers name a file. I counted the answer text, not the `Sources retrieved` line, because that line is printed by retrieval whether the model uses it or not. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused against a target of 4 of 5. The closest out-of-scope question scored 0.828 against a 0.6 cutoff, so nothing was near the boundary. |
| 4 | No chunk is cut mid-sentence | MET | 0 of 23 across the whole index, not a sample. Checked both ends of every chunk: none starts mid-reply, none ends without sentence-final punctuation. |
| 5 | No in-scope question comes back refused | MET | 0 refusals of 5. Checked by the rule I wrote in criteria.md — the literal phrase "don't have enough information" in the printed answer — rather than by reading for tone. |

All five met, which I want to be careful about rather than pleased with.

**Criterion 1 is the one that actually tells me something.** I wrote it
expecting to spend my one allowed miss on "When do small local employers hire
summer interns?", because its answer is a single month inside a threaded reply
and my old 800-character chunker was severing three chunks mid-sentence. It
came back at rank 1, distance 0.3418, in all three runs. That isn't the target
being loose — it's the Milestone 3 chunker fix landing on exactly the question
I'd predicted it would rescue. The prediction and the repair are two entries in
criteria.md written a day apart, and this run is where they met.

**Criteria 1 and 5 were supposed to fail together and didn't.** I'd written
that if retrieval missed the internship question, the model would get chunks
without the month in them and would correctly refuse, taking criterion 5 down
with criterion 1. Since retrieval didn't miss, that link was never tested. I
don't get to claim credit for criterion 5 surviving a pressure it never came
under.

**Where this leaves the targets.** Three of the five passed by a margin wide
enough that I should say plainly they were not hard: criterion 3's nearest miss
is 0.23 from the cutoff, and criterion 4 now holds by construction rather than
by measurement — the chunker cannot split inside a reply, so there is no run in
which that row comes back non-zero. Which of these I'd tighten, and to what,
belongs in Diagnoses below.

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

**I missed nothing. All five criteria were met on the first run.** So there is
no stage-and-mechanism story to tell about a failure, and the honest version of
this section is about the measurement rather than the system.

**The targets were safe.** Not all equally, and the way they were safe has a
single cause rather than five.

Four of my five criteria are scored over questions I wrote myself, after
reading the corpus, knowing what it contained. Criteria 1, 2 and 5 all run over
the same five in-scope questions, and criterion 3 runs over five out-of-scope
ones I picked to be obviously outside it. That is one problem, not four: my test
set was built to be answerable, so it measured whether the pipeline works on
easy cases and never went looking for the edge.

### The pattern: my gate was never tested on a hard question

My five OUT_OF_SCOPE questions are the capital of Mongolia, the 1994 World Cup,
diesel oil changes, ibuprofen dosage, and Rust syntax. Nothing about a
university. That is what produced the "0.4074 gap with nothing in it" I leaned
on above, and the claim that 0.6 "sits in open space".

I tested that claim by writing seven questions that are campus-adjacent but
genuinely not in my 23 threads, and running them through `app.py retrieve`,
which costs no model calls:

| Near-miss question | Best distance | Nearest thread | Gate at 0.6 |
|---|---|---|---|
| How much does a load of laundry cost? | 0.5286 | `thread_laundry_timing.txt` | **passed** |
| What are the best dorms to live in? | 0.5794 | `thread_study_spots.txt` | **passed** |
| Where is the campus gym and what are its hours? | 0.5826 | `thread_study_spots.txt` | **passed** |
| How do I book a counselling appointment? | 0.6201 | `thread_sleep_schedule.txt` | refused |
| Is the dining hall open on weekends? | 0.6569 | `thread_study_spots.txt` | refused |
| How do I apply for financial aid? | 0.6854 | `thread_first_gen.txt` | refused |
| What is the wifi password on campus? | 0.7651 | `thread_study_spots.txt` | refused |

**The band I called empty is populated, and it straddles my cutoff.** Three
out-of-corpus questions get through a 0.6 gate. The mechanism is the stage I
never suspected — embedding, not retrieval or chunking. `thread_study_spots.txt`
is the nearest neighbour for four of these seven, because "campus", "building"
and "hours" put a question in its neighbourhood regardless of what the question
is actually asking. `thread_laundry_timing.txt` is about *when machines are
free*, never about price, and a question about cost still lands 0.5286 from it.
Topic proximity is not answer containment, and a distance score cannot tell them
apart.

Criterion 3 is still honestly MET — my five OUT_OF_SCOPE questions really were
all refused. The finding is that the test could not have discovered this.

### The one thing the passes did tell me

Two of those three leaked questions reached the model, which is the second
refusal site I described in criterion 5 and said I don't control. It held:

```
  (best distance 0.529, cutoff 0.6)

Based on the provided documents, there is no mention of how much a load of laundry costs (source: `thread_laundry_timing.txt`).
```

That is `generate.py::answer_from_chunks` catching what the gate let past — the
grounding instruction doing the job the distance score couldn't.

It also exposes a hole in my own scoring. Criterion 5 counts a question as
refused only if the answer contains the literal phrase "don't have enough
information". That answer is a refusal and does not contain the phrase. My
0-of-5 for criterion 5 is correct, but the rule that produced it would have
missed a real refusal if one had happened — so that number is right by luck.

### Which criterion I'd tighten, and to what

**Criterion 3**, from *"at least 4 of 5 out-of-corpus questions refused"* to:

> 5 of 5 refused, where at least 3 of the out-of-scope questions are
> campus-adjacent topics my corpus does not cover, and no out-of-scope question
> scores below 0.65.

That version fails on today's numbers, which is the point — the current version
cannot fail. This is the criterion my improvement below goes after.

Two smaller ones I'd also change, and did not: **criterion 1** should require the
answer-bearing chunk at **rank 1**, not anywhere in the top 3, because rank 1 was
already the right thread for all five questions while rank 3 never drops below
0.7386 — I was scoring a bar three times looser than what my retrieval does.
And **criterion 4** I would retire rather than tighten: the reply-boundary
splitter cannot produce a mid-sentence chunk, so 0 of 23 restates the chunker's
design instead of measuring anything. A number that cannot move is not worth a
row.

## The Improvement

**What I changed:**

One line in `config.py`: `THRESHOLD` from **0.6 to 0.475**. Nothing else — same
chunker, same top-k of 3, same grounding instruction, same corpus, same
questions.

**Why I picked it:**

My diagnosis found three out-of-corpus questions clearing a 0.6 gate at
0.5286–0.5826, so I moved the cutoff into the gap that actually separates my
in-scope questions from out-of-corpus ones rather than the gap I had measured
against absurd questions.

I did not pick hybrid search or a second chunking strategy. Both were on the
list and both are more interesting, but neither addresses what I found: my
retrieval already returns the right thread at rank 1 for every in-scope
question, so ranking was not the problem. The gate was.

**Where 0.475 comes from.** My in-scope five top out at 0.4206 (the bike
question). The nearest out-of-corpus question is laundry cost at 0.5286. That
is the real gap — 0.108 wide, not the 0.4074 I originally claimed — and 0.475
is its midpoint. The old 0.6 sat *inside* the out-of-corpus group rather than
between the groups.

| | Old gate (0.6) | New gate (0.475) |
|---|---|---|
| In-scope questions passed | 5 of 5 | 5 of 5 |
| OUT_OF_SCOPE refused | 5 of 5 | 5 of 5 |
| Near-miss questions refused | 4 of 7 | **7 of 7** |
| Margin below cutoff for worst in-scope | 0.179 | **0.054** |

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk is cut mid-sentence | 0 of 23 | 0 of 23 | 0 of 23 | 0 of 23 | MET |
| 5. No in-scope question comes back refused | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | MET |

Source run: `results/run_2026-09-29_0032_after.md`, written by `run_eval.py::main`
on 2026-09-29 — corpus `advice_threads`, top-k 3, cutoff **0.475**, three runs
per question, caching off. 15 model calls, 10353 tokens. Same aggregation as the
before table: one row per criterion, from a file that is one row per question.
Criteria 3 and 4 are measured in one pass for the reasons given above.

`scorer.py` doesn't exist yet, so `run_eval.py` left its own verdict column
blank and printed `—` for each run. Every judgement in the table above is mine,
made by reading the 15 answers in the run file against the rules in
`criteria.md`.

### Real output

**Criterion 1 — the answer-bearing thread came back every time.** Scored off the
`Sources retrieved` line. Rank 1 was the correct thread for all five questions in
all three runs, unchanged from before:

```
### When do small local employers hire summer interns? — run 1

- Best distance: 0.3418 (passed the gate)
- Sources retrieved: thread_first_gen.txt, thread_internship_timing.txt, thread_laundry_timing.txt
```

**Criterion 2 — 15 of 15 answers name a file.** Still in three different formats,
because the model picks its own:

```
Small and local places hire summer interns in February and March (*thread_internship_timing.txt*).
```

```
You need 16GB of RAM, as 8GB may struggle by the final project and 16GB is considered the number worth paying for. This comes from `thread_laptop_specs.txt`.
```

```
No, it is not weird to go to office hours without a specific question; saying something like "I'm following the lectures but I don't feel like I understand the shape of it" is completely normal. 

This comes from *thread_office_hours_etiquette.txt*.
```

**Criterion 3 — 5 of 5 refused**, at 0.828–0.952 against the new 0.475 cutoff.
The same five questions, further from the gate than before because the gate
moved toward them.

**Criterion 4 — 0 of 23.** The index was not rebuilt; `THRESHOLD` is read at
query time and the chunker never ran. This row is carried over unchanged, which
is itself the argument in Diagnoses for retiring it.

**Criterion 5 — 0 refusals of 5.** Closest call is the bike question at 0.4206
against 0.475: **0.054 of margin**, down from 0.179.

**Did it help?**

**Not by anything in the table above, and the table is the wrong place to look
for it.**

All five criteria read identically before and after — 5/5, 5/5, 5/5, 0/23, 0/5.
So do the distances, to four decimal places: 0.2869, 0.3287, 0.3418, 0.3898,
0.4206 in both runs. That isn't a coincidence and it isn't a null result. A
threshold is a comparison applied *after* retrieval; it cannot move an embedding
distance, so the only thing it can change is which side of the line a question
falls on. None of my ten test questions changed sides, because all ten were
already sorted correctly. **The change was invisible to my test suite by
construction.**

What it did change is measurable, just not here:

| | Old gate (0.6) | New gate (0.475) |
|---|---|---|
| The five criteria above | all MET | all MET — no movement |
| Near-miss questions refused | 4 of 7 | **7 of 7** |
| Margin below cutoff for worst in-scope | 0.179 | **0.054** |

The three questions that changed behaviour — laundry cost at 0.5286, best dorms
at 0.5794, gym hours at 0.5826 — are the ones from my Diagnoses section, and
they are not in `questions.py`. So the honest summary is: **the fix worked on
the failure I found, and my test suite cannot see it.** I'd rather report that
than quietly add the near-miss questions to `OUT_OF_SCOPE` and present a
5-of-5 that the before run never had a chance to score.

It also cost something real. The worst in-scope question now clears the gate by
0.054 instead of 0.179. I traded margin I wasn't using against absurd questions
for margin against plausible ones, which is the right trade on this corpus, but
it is a trade and not a free win. If a legitimate in-scope question ever gets
refused, this is the line that did it.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Against the five targets I wrote in unit 1, nothing is missed — they were all
met before the fix and all met after it. So this section is about the tightened
criterion 3 I proposed in Diagnoses, and about three things the run log does not
show.

**1. Criterion 3, under the definition I'd tighten it to, still fails.** The
second half of that target was "no out-of-scope question scores below 0.65". My
near-miss questions sit at 0.5286, 0.5794 and 0.5826. They are refused now, but
only because the cutoff moved to meet them — they are still closer to my corpus
than a question my corpus cannot answer should be.

*What I'd do:* this is an embedding problem, not a threshold one, and moving the
number again won't fix it. `thread_study_spots.txt` is the nearest neighbour for
four of seven near-miss questions because shared campus vocabulary dominates the
similarity score. The fix I'd try is the hybrid search option — BM25 alongside
the embedding — on the theory that a keyword leg would score "gym", "dorms" and
"wifi" near zero against a corpus that never uses those words, where the
embedding gives them 0.55.

*Why I stopped:* that is a second change, and the milestone asks for one. I'd
rather report a small change I can attribute cleanly than two changes and no way
to tell which did the work.

**2. The new gate has very little margin.** The bike question passes at 0.4206
against a 0.475 cutoff — 0.054 of room, down from 0.179. I chose the midpoint of
a 0.108-wide gap, and a gap that narrow means the next question I write could
land on either side of it. The old cutoff was safe and wrong; this one is
correct and fragile. If a genuinely in-scope question ever gets refused, this is
why, and criterion 5 is where it will show up.

*Why I stopped:* the alternative is widening the gap rather than re-placing the
cutoff inside it, which again means changing retrieval.

**3. My near-miss questions aren't in the test.** They live in this README, not
in `OUT_OF_SCOPE` in `questions.py`, so `run_eval.py` doesn't score them and a
future change could silently undo this fix. I left them out deliberately —
adding them would have changed what criterion 3 measures in the middle of a
before/after comparison, and the two run logs would not be comparable. They
should go in before any further work.

**4. Criterion 5's scoring rule can't be trusted.** It matches the literal
phrase "don't have enough information", and I have a real refusal from this unit
that doesn't contain it. Every 0-of-5 I've recorded for criterion 5 is correct,
but none of them is *evidence*, because the check would have returned 0 whether
the model refused or not.

*Why I stopped:* fixing it means rewriting a criterion mid-unit, and the whole
point of writing them first is that I don't get to edit them once I've seen the
results. It goes in the next unit's version.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

**Criterion 3 — the one I'd change first.** Not the target number, the question
set behind it. I wrote five out-of-scope questions about Mongolia, the World Cup
and diesel engines, and they told me nothing: no system that retrieves anything
at all would fail them. A refusal test is only worth running on questions that
are *nearly* in scope. I'd require that most of the out-of-scope set be
same-domain-different-topic, and I'd write those questions before measuring any
distances, so I couldn't unconsciously pick ones I knew would sort cleanly.

**Criterion 1 — I scored a bar three times looser than my system.** "In the top
3" made sense when top-k was 5 and I hadn't measured anything. By the time I ran
it, rank 1 was the correct thread for all five questions and rank 3 never came
back under 0.7386. I'd write "rank 1" and accept that it's harder, because it's
what the system actually does and it would catch a regression that "top 3"
would hide.

**Criterion 4 — I'd write it so it can fail.** "No chunk is cut mid-sentence"
became unfalsifiable the moment I replaced the chunker with one that splits on
reply boundaries; the splitter cannot produce the failure. I'd replace it with
something that is still a real question after the fix — every chunk answerable
without its neighbours, say, which I'd have to read the chunks to judge and
could genuinely lose.

**The general lesson.** Four of my five criteria were scored on inputs I chose
after reading the corpus, and all five passed first time. I'd treated writing
the criteria first as the safeguard, but writing them first doesn't help if I
also write the test data. Next unit I'd fix the *questions* before I look at the
documents, not just the targets.
